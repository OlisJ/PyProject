from pydantic import BaseModel

class GameCreate(BaseModel):
    name: str
    description: str
    price: float
    genre: str
    release_date: str


class Game(BaseModel):
    id:int