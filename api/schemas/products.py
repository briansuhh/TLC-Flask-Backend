from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Int(required=True, attribute="product_id")
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    variant_group_id = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    category_id = fields.Int(required=True)