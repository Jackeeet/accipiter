import importlib
from typing import Callable

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dependencies import auth_config, update_block


class Password(BaseModel):
    value: str


router = APIRouter(prefix="/settings")


@router.get("/admin_pass")
async def get_admin_password(cfg: dict = Depends(auth_config)):
    return cfg["admin_password"]


@router.post("/admin_pass")
async def set_admin_password(
        password: Password, cfg: dict = Depends(auth_config), updater: Callable = Depends(update_block)
):

    cfg["admin_password"] = password.value
    updater("auth", cfg)
    import dependencies.config_manager
    importlib.reload(dependencies.config_manager)
    return {"message": "Updated admin password"}

