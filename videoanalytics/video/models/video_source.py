from pydantic import BaseModel


class VideoSource(BaseModel):
    path: str
