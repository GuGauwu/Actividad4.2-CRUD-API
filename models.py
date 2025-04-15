from sqlalchemy import Column, Integer, String, Float
from database import Base

class VideoGame(Base):
    __tablename__ = "videojuegos"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    consola = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
