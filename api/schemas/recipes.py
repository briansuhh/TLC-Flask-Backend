from marshmallow import Schema, fields

class RecipeSchema(Schema):
    product_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    quantity = fields.Float(required=True)
    isTakeout = fields.Bool(required=True)
