import sys

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from dependencies import editor_config

router = APIRouter(prefix="/editor")


@router.get("/object_list")
async def object_list(cfg: dict = Depends(editor_config)):
    return FileResponse(sys.path[0] + cfg["object_list_path"])
