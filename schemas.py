from pydantic import BaseModel

class VideoGameBase(BaseModel):
    titulo: str
    consola: str
    precio: float
    stock: int

class VideoGameCreate(VideoGameBase):
    pass

class VideoGame(VideoGameBase):
    id: int
    class Config:
        orm_mode = True
