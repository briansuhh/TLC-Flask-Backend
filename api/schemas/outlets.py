from marshmallow import Schema, fields, validate

class OutletSchema(Schema):
    id = fields.Int(dump_only=True, attribute="outlet_id")
    product_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    price = fields.Float(required=True)