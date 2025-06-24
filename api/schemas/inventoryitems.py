from marshmallow import Schema, fields, validate

class InventorySchema(Schema):
    id = fields.Int(required=True, attribute="item_id")
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    cost = fields.Float(required=True)
    unit = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    stock_warning_level = fields.Float(required=True)
    supplier_id = fields.Int(required=True)
