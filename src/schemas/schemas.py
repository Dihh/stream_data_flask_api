from marshmallow import Schema, fields


class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)

class SystemDateSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.DateTime(required=True)

class ViewersSchema(Schema):
    id = fields.Int(dump_only=True)
    viewers = fields.Integer(required=True)
    system_date_id = fields.Integer(required=True)
    game_id = fields.Integer(required=True)

class DetailedViewersSchema(Schema):
    id = fields.Int(dump_only=True)
    viewers = fields.Integer(required=True)
    system_date = fields.Pluck("SystemDateSchema", "date")
    game = fields.Pluck("GameSchema", "name")

class DatiledGameSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    viewers = fields.Nested(DetailedViewersSchema(many=True))
