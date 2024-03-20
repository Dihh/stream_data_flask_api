from sqlalchemy.orm import declarative_base

from db import db

Base = declarative_base()

class GameModel(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    viewers = db.relationship("ViewerModel", back_populates="game", lazy="dynamic")
