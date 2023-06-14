import importlib
import sys
from typing import Callable

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from dependencies import logs_config, update_block

router = APIRouter(prefix="/logs")


@router.get("/log_alerts")
async def get_log_alerts_value(cfg: dict = Depends(logs_config)):
    return {"value": cfg["log_alerts"]}


@router.post("/log_alerts")
async def set_log_alerts_value(
        value: bool,
        cfg: dict = Depends(logs_config), updater: Callable = Depends(update_block)
):
    cfg["log_alerts"] = value
    updater("logs", cfg)
    import dependencies.config_manager
    importlib.reload(dependencies.config_manager)
    return {"message": f"Set 'log_alerts' to {value}"}


@router.get("/{log_name}")
async def get_log_contents(log_name: str, cfg: dict = Depends(logs_config)):
    path = _log_name_to_path(log_name, cfg)
    return FileResponse(sys.path[0] + path)


@router.delete("/{log_name}")
async def clear_log_contents(log_name: str, cfg: dict = Depends(logs_config)):
    path = _log_name_to_path(log_name, cfg)
    open(sys.path[0] + path, 'w').close()


@router.get("/")
async def log_file_list():
    return [
        ["Журнал событий"],
        ["Журнал оповещений"],
        ["Журнал ошибок"]
    ]


def _log_name_to_path(log_name: str, cfg: dict = Depends(logs_config)) -> str:
    match log_name:
        case "Журнал событий":
            return cfg["event_log_path"]
        case "Журнал оповещений":
            return cfg["alert_log_path"]
        case "Журнал ошибок":
            return cfg["error_log_path"]
        case _:
            raise ValueError("invalid log name")
