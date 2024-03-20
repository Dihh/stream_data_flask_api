from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import ViewersSchema, DetailedViewersSchema
from src.models import ViewerModel
from db import db

blp = Blueprint("viewers", __name__)

@blp.route("/viewers/<string:viewer_id>")
class ViewerController(MethodView):
    @blp.response(200, DetailedViewersSchema )
    def get(self, viewer_id):
        viewer = ViewerModel.query.get_or_404(viewer_id)
        return viewer


@blp.route("/viewers")
class ViewersController(MethodView):

    @blp.arguments(ViewersSchema(many=True))
    @blp.response(201, ViewersSchema(many=True))
    def post(self, viewer_data):
        viewer = [ViewerModel(**data) for data in viewer_data]
        try:
            db.session.add_all(viewer)
            db.session.commit()
        except SQLAlchemyError:
            abort(500)
        return viewer, 201
