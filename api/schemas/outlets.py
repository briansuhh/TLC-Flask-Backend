from marshmallow import Schema, fields, validate

class OutletSchema(Schema):
    product_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    price = fields.Float(required=True)