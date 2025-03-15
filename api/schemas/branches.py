from marshmallow import Schema, fields, validate

class BranchSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    address = fields.Str(required=True, validate=validate.Length(max=100))
