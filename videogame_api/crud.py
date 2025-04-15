from sqlalchemy.orm import Session
from models import VideoGame
from schemas import VideoGameCreate

def get_games(db: Session):
    return db.query(VideoGame).all()

def get_game(db: Session, game_id: int):
    return db.query(VideoGame).filter(VideoGame.id == game_id).first()

def create_game(db: Session, game: VideoGameCreate):
    db_game = VideoGame(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def update_game(db: Session, game_id: int, game: VideoGameCreate):
    db_game = db.query(VideoGame).filter(VideoGame.id == game_id).first()
    if db_game:
        for attr, value in game.dict().items():
            setattr(db_game, attr, value)
        db.commit()
        db.refresh(db_game)
    return db_game

def delete_game(db: Session, game_id: int):
    db_game = db.query(VideoGame).filter(VideoGame.id == game_id).first()
    if db_game:
        db.delete(db_game)
        db.commit()
    return db_game
