from marshmallow import Schema, fields, validate

class SupplierSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    phone = fields.Str(required=True, validate=validate.Length(max=11))
    country_code = fields.Str(required=True, validate=validate.Length(max=4))