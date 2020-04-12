from marshmallow import Schema, fields


class RegisterParameters(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class ProfileParameters(Schema):
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    about_me = fields.String(required=True)