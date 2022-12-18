import json
import os
import sys
from io import TextIOWrapper
from typing import Callable

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import FileResponse

from dependencies import rule_config

router = APIRouter(prefix="/rules")


@router.get("")
async def get_file_names(cfg: dict = Depends(rule_config)):
    return await _access_db(cfg, action=_sort_items, check=None, filename=None)


@router.get("/{filename}")
async def get_file(filename: str, cfg: dict = Depends(rule_config)):
    await _access_db(cfg, action=None, check=_filename_exists, filename=filename)
    stored_file = sys.path[0] + cfg["files_dir"] + filename
    return FileResponse(stored_file)


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile, cfg: dict = Depends(rule_config)):
    await _upload_file(file, file.filename, cfg)
    await _access_db(cfg, action=_add_filename, check=_filename_doesnt_exist, filename=file.filename)
    return {"message": f"Successfully uploaded {file.filename}"}


@router.post("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def update_file(filename: str, file: UploadFile, cfg: dict = Depends(rule_config)):
    if filename != file.filename:
        raise HTTPException(status_code=409, detail="Filename mismatch")
    await _access_db(cfg, action=None, check=_filename_exists, filename=filename)
    await _upload_file(file, filename, cfg)
    return {"message": f"Successfully updated {filename}"}


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(filename: str, cfg: dict = Depends(rule_config)):
    await _access_db(cfg, action=_delete_filename, check=_filename_exists, filename=filename)
    try:
        os.remove(sys.path[0] + cfg["files_dir"] + filename)
    except OSError as ex:
        raise HTTPException(status_code=409, detail=f"Could not delete the file: {ex}")


async def _access_db(cfg: dict, action: Callable = None, check: Callable = None, filename: str = None):
    db_file = sys.path[0] + cfg["db_file"]
    try:
        with open(db_file, "r+") as dbf:
            db = json.load(dbf)
            if check is not None:
                check(filename, db)
            if action is not None:
                result = await action(dbf, filename, db)
                return result

    except FileNotFoundError:
        raise HTTPException(status_code=409, detail=f"Could not access the file database.")


def _filename_exists(filename: str, db: list[str]):
    if filename not in db:
        raise HTTPException(status_code=409, detail=f"A file with the name {filename} does not exist.")


def _filename_doesnt_exist(filename: str, db: list[str]):
    if filename in db:
        raise HTTPException(status_code=409, detail=f"A file with the name {filename} already exists.")


async def _sort_items(db_file, filename, db: list[str]):
    return sorted(db)


async def _delete_filename(db_file: TextIOWrapper, filename: str, db: list[str]):
    db.remove(filename)
    _rewrite_db(db_file, db)


async def _add_filename(db_file: TextIOWrapper, filename: str, db: list[str]):
    db.append(filename)
    _rewrite_db(db_file, db)


async def _upload_file(file: UploadFile, filename: str, cfg: dict):
    # todo check file extension
    try:
        contents = file.file.read()
        storage_path = sys.path[0] + cfg["files_dir"] + filename
        with open(storage_path, 'wb') as f:
            f.write(contents)
    except OSError as ex:
        return {"message": f"Could not upload the file: {ex}"}
    finally:
        file.file.close()


def _rewrite_db(db_file: TextIOWrapper, contents: list[str]):
    db_file.seek(0)
    db_file.write(json.dumps(contents))
    db_file.truncate()
