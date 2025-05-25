from marshmallow import Schema, fields, validate

class BranchStockCountSchema(Schema):
    branch_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    in_stock = fields.Float(required=True)
    ordered_qty = fields.Float(required=True)
