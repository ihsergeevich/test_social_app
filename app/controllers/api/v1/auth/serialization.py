from marshmallow import Schema, fields


class AuthParameters(Schema):
    login = fields.String(required=True)
    password = fields.String(required=True)


class RefreshParameters(Schema):
    refresh_token = fields.String(required=True)

