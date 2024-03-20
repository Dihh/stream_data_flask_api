from sqlalchemy.orm import declarative_base

from db import db

Base = declarative_base()

class ViewerModel(db.Model):
    __tablename__ = "viewers"

    id = db.Column(db.Integer, primary_key=True)
    viewers = db.Column(db.Integer(), nullable=False)

    system_date_id = db.Column(db.Integer(), db.ForeignKey("system_dates.id"), nullable=False)
    game_id = db.Column(db.Integer(), db.ForeignKey("games.id"), nullable=False)

    game = db.relationship("GameModel", back_populates="viewers")
    system_date = db.relationship("SystemDateModel", back_populates="viewers")
