from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models, crud, schemas
from database import SessionLocal, engine

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cambiado a 'frontend' en lugar de 'templates'
templates = Jinja2Templates(directory="frontend")

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz que sirve index.html desde la carpeta frontend
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Crear videojuego
@app.post("/videojuegos/", response_model=schemas.VideoGame)
def create_videogame(game: schemas.VideoGameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, game)

# Leer todos los videojuegos
@app.get("/videojuegos/", response_model=list[schemas.VideoGame])
def read_videogames(db: Session = Depends(get_db)):
    return crud.get_games(db)

# Leer un videojuego por ID
@app.get("/videojuegos/{game_id}", response_model=schemas.VideoGame)
def read_videogame(game_id: int, db: Session = Depends(get_db)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return game

# Actualizar videojuego
@app.put("/videojuegos/{game_id}", response_model=schemas.VideoGame)
def update_videogame(game_id: int, game: schemas.VideoGameCreate, db: Session = Depends(get_db)):
    return crud.update_game(db, game_id, game)

# Eliminar videojuego
@app.delete("/videojuegos/{game_id}")
def delete_videogame(game_id: int, db: Session = Depends(get_db)):
    return crud.delete_game(db, game_id)
