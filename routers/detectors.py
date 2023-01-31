import json
import sys
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from dependencies import detectors_config

router = APIRouter(prefix="/detectors")


@router.get("")
async def get_detector_names(cfg: dict = Depends(detectors_config)):
    db = await _access_db(cfg)
    return list(db["filenames"].items())


@router.get("/{sys_filename}")
async def get_file(sys_filename: str, cfg: dict = Depends(detectors_config)):
    # db = await _access_db(cfg)
    # todo check if file exists
    stored_file = sys.path[0] + cfg["files_dir"] + sys_filename.replace("-", "/")
    return FileResponse(stored_file)


async def _access_db(cfg: dict, action: Callable = None, check: Callable = None, filename: str = None):
    db_file = sys.path[0] + cfg["db_file"]
    try:
        with open(db_file, "r+", encoding="utf-8") as dbf:
            db = json.load(dbf)
            if check is not None:
                check(filename, db)
            if action is not None:
                await action(dbf, filename, db)
            return db
    except FileNotFoundError:
        raise HTTPException(status_code=409, detail=f"Could not access the file database.")
