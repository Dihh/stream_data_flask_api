from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import SystemDateSchema
from src.models import SystemDateModel
from db import db

blp = Blueprint("system_dates", __name__)

@blp.route("/system_dates")
class SystemDateController(MethodView):

    @blp.response(200, SystemDateSchema(many=True) )
    def get(self):
        games = SystemDateModel.query.all()
        return games, 201


    @blp.arguments(SystemDateSchema(many=True))
    @blp.response(201, SystemDateSchema(many=True))
    def post(self, date_data):
        date = [SystemDateModel(**data) for data in date_data]
        try:
            db.session.add_all(date)
            db.session.commit()
        except SQLAlchemyError:
            abort(500)
        return date, 201
