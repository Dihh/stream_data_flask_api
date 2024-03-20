from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import GameSchema, DatiledGameSchema
from src.models.game import GameModel
from db import db

blp = Blueprint("games", __name__)

@blp.route("/games/<string:game_id>")
class GameController(MethodView):
    @blp.response(200, DatiledGameSchema )
    def get(self, game_id):
        game = GameModel.query.get_or_404(game_id)
        return game


@blp.route("/games")
class GamesController(MethodView):

    @blp.response(200, GameSchema(many=True) )
    def get(self):
        games = GameModel.query.all()
        return games


    @blp.arguments(GameSchema(many=True))
    @blp.response(201, GameSchema(many=True))
    def post(self, games_data):
        games = [GameModel(**game_data) for game_data in games_data]
        try:
            db.session.add_all(games)
            db.session.commit()
        except SQLAlchemyError:
            abort(500)
        return games, 201
