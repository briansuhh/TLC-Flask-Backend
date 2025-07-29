from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    id = fields.Int(dump_only=True, attribute="category_id")
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
