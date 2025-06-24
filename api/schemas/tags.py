from marshmallow import Schema, fields, validate

class TagSchema(Schema):
    id = fields.Int(required=True, attribute="tag_id")
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    