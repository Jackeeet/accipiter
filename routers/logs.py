from fastapi import APIRouter

router = APIRouter(prefix="/logs")


@router.get("/")
async def log_file_list():
    return [
        ["Журнал событий"],
        ["Журнал оповещений"],
        ["Журнал ошибок"]
    ]
