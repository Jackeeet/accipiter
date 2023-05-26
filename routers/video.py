import importlib
from typing import Callable

from fastapi import APIRouter, Depends

from dependencies import video_source, update_video_source
from videoanalytics.video.models.video_source import VideoSource

router = APIRouter(prefix="/video")


@router.get("/source")
async def get_source_path(src: str = Depends(video_source)):
    return src


@router.post("/source")
async def set_source_path(source: VideoSource, updater: Callable = Depends(update_video_source)):
    updater("video_source", source.path)
    import dependencies.config_manager
    importlib.reload(dependencies.config_manager)
    return {"message": f"Successfully set source to {source.path}"}
