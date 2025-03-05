from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    middle_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    birth_date = fields.Date(required=True)
    sex = fields.Str(required=True, validate=validate.OneOf(['M', 'F']))
    position = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))
