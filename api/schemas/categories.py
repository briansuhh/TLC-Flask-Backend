from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
