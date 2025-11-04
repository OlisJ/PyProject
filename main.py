from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn
import database
import models
from models import Game,GameCreate


app=FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Games CRUD API"}


@app.post("/Games/" , response_model=Game)
def create_game(game:GameCreate):
    game_id = database.create_game(game)
    return models.Game(id=game_id , **game.dict())


@app.get("/Games/", response_model=List[Game])
def read_games():
    return database.read_games()


@app.get("/Games/{game_id}" , response_model=Game)
def read_game(game_id: int):
    game = database.read_game(game_id)  
    if game is None:
       raise HTTPException(status_code=404 , detail="Game NOT FOUND ")
    return game


@app.put("/Games/{game_id}" , response_model=Game)
def update_game(game_id: int , game:GameCreate):
    updated = database.update_game(game_id , game)
    if not updated:
        raise HTTPException(status_code=404 , detail="Game not found")
    return models.Game(id=game_id , **game.dict())


@app.delete("/Games/{game_id}" , response_model=dict)
def delete_game(game_id:int):
    deleted = database.delete_game(game_id)
    if not deleted:
        raise HTTPException(status_code=404 , detail="Game not found")
    return {"message": "Game deleted successfully"}