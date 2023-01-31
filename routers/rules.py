import importlib
import json
import os
import sys
from io import TextIOWrapper
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile
from fastapi.responses import FileResponse

from dependencies import rule_config, update_block

from redpoll.translator import TranslationError, Translator

router = APIRouter(prefix="/rules")


@router.get("/active")
async def active_file(cfg: dict = Depends(rule_config)):
    return cfg["active_file"]


@router.post("/active/{filename}", status_code=200)
async def set_active_file(filename: str,
                          response: Response,
                          cfg: dict = Depends(rule_config),
                          cfg_updater: Callable = Depends(update_block)):
    await _access_db(cfg, action=None, check=_filename_exists, filename=filename)

    input_file = sys.path[0] + cfg["files_dir"] + filename
    output_file = sys.path[0] + cfg["translated_rules_path"]
    translator = Translator(input_file, output_file)
    try:
        translator.translate()
    except TranslationError as t_err:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'message': str(t_err)}

    output_module = 'videoanalytics.analytics.declared'
    if output_module in sys.modules:
        import videoanalytics.analytics.declared
        importlib.reload(videoanalytics.analytics.declared)

    cfg["active_file"] = filename
    cfg_updater("rules", cfg)
    return {'message': 'Successfully set active file'}


@router.get("/check/{filename}")
async def file_exists(filename: str, cfg: dict = Depends(rule_config)):
    exists = await _file_in_db(cfg, filename)
    return {"exists": exists}


@router.get("")
async def get_file_names(cfg: dict = Depends(rule_config)):
    db = await _access_db(cfg)
    return [[filename, filename] for filename in db]


@router.get("/{filename}")
async def get_file(filename: str, cfg: dict = Depends(rule_config)):
    await _access_db(cfg, action=None, check=_filename_exists, filename=filename)
    stored_file = sys.path[0] + cfg["files_dir"] + filename
    return FileResponse(stored_file)


@router.post("")
async def upload(file: UploadFile, cfg: dict = Depends(rule_config)):
    await _upload_file(file, file.filename, cfg)
    await _access_db(cfg, action=_add_filename, check=None, filename=file.filename)
    return {"message": f"Successfully uploaded {file.filename}"}


@router.delete("/{filename}")
async def delete_file(filename: str, cfg: dict = Depends(rule_config)):
    filenames = await _access_db(cfg, action=_delete_filename, check=_filename_exists, filename=filename)
    try:
        os.remove(sys.path[0] + cfg["files_dir"] + filename)
        return filenames
    except OSError as ex:
        await _access_db(cfg, action=_add_filename, check=None, filename=filename)
        raise HTTPException(status_code=409, detail=f"Could not delete the file: {ex}")


async def _access_db(cfg: dict, action: Callable = None, check: Callable = None, filename: str = None):
    db_file = sys.path[0] + cfg["db_file"]
    try:
        with open(db_file, "r+") as dbf:
            db = json.load(dbf)
            if check is not None:
                check(filename, db)
            if action is not None:
                await action(dbf, filename, db)
            return db
    except FileNotFoundError:
        raise HTTPException(status_code=409, detail=f"Could not access the file database.")


async def _file_in_db(cfg: dict, filename: str) -> bool:
    """ Opens the db file and checks if the filename exists. """
    db_file = sys.path[0] + cfg["db_file"]
    try:
        with open(db_file, "r+") as dbf:
            db = json.load(dbf)
            return filename in db
    except FileNotFoundError:
        raise HTTPException(status_code=409, detail=f"Could not access the file database.")


# ---- Checks ----
def _filename_exists(filename: str, db: list[str]):
    """ Checks if the filename exists in a db file that's already open. """
    if filename not in db:
        raise HTTPException(status_code=409, detail=f"A file with the name {filename} does not exist.")


# ---- Actions ----
async def _delete_filename(db_file: TextIOWrapper, filename: str, db: list[str]):
    if filename in db:
        db.remove(filename)
        _rewrite_db(db_file, db)
    # perhaps filename not being in db should be an error


async def _add_filename(db_file: TextIOWrapper, filename: str, db: list[str]):
    if filename not in db:
        db.append(filename)
        _rewrite_db(db_file, db)
    # if it's already in the database, do nothing


# ---- Helpers ----
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
    db_file.write(json.dumps(sorted(contents)))
    db_file.truncate()
