from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    item_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    retail_price = fields.Float(required=True)
    wholesale_price = fields.Float(required=True)
    category = fields.Str(required=True)
    vendor = fields.Str(required=True)


class PlainWarehouseSchema(Schema):
    id = fields.Int(dump_only=True)   # Make sure warehouse_id doesn't need to be named id
    name = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    item_id = fields.Int()
    name = fields.Str()
    retail_price = fields.Float()
    wholesale_price = fields.Float()
    category = fields.Str()
    vendor = fields.Str()
    warehouse = fields.Str()
    warehouse_id = fields.Int()
    quantity = fields.Integer()


class ItemSchema(PlainItemSchema):
    warehouse_id = fields.Int(required=True, load_only=True)
    warehouse = fields.Nested(PlainWarehouseSchema(), dump_only=True)
    quantity = fields.Integer(required=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class WarehouseSchema(PlainWarehouseSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    warehouse_id = fields.Int(load_only=True)
    warehouse = fields.Nested(PlainWarehouseSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)