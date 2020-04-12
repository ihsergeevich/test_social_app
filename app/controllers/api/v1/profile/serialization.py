from marshmallow import Schema, fields


class UserProfileParameters(Schema):
    request_user_id = fields.Integer(required=True)
