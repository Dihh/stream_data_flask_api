from sqlalchemy.orm import declarative_base

from db import db

Base = declarative_base()

class SystemDateModel(db.Model):
    __tablename__ = "system_dates"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)

    viewers = db.relationship("ViewerModel", back_populates="system_date", lazy="dynamic")
