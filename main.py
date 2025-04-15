from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/videojuegos/", response_model=schemas.VideoGame)
def create_videogame(game: schemas.VideoGameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, game)

@app.get("/videojuegos/", response_model=list[schemas.VideoGame])
def read_videogames(db: Session = Depends(get_db)):
    return crud.get_games(db)

@app.get("/videojuegos/{game_id}", response_model=schemas.VideoGame)
def read_videogame(game_id: int, db: Session = Depends(get_db)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return game

@app.put("/videojuegos/{game_id}", response_model=schemas.VideoGame)
def update_videogame(game_id: int, game: schemas.VideoGameCreate, db: Session = Depends(get_db)):
    return crud.update_game(db, game_id, game)

@app.delete("/videojuegos/{game_id}")
def delete_videogame(game_id: int, db: Session = Depends(get_db)):
    return crud.delete_game(db, game_id)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para desarrollo puedes dejarlo así
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
