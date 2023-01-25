from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="operations on items")


@blp.route("/item/<int:item_id>")                # http://127.0.0.1:5000/item/<item_id>
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):                         # Retrieve an item
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):                       # Delete an item
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):                # Update an item
        item = ItemModel.query.get(item_id)
        if item:
            item.retail_price = item_data["retail_price"]
            item.wholesale_price = item_data["wholesale_price"]
            item.category = item_data["category"]
            item.description = item_data["description"]
            item.vendor = item_data["vendor"]
            item.warehouse_id = item_data["warehouse_id"]
            item.quantity = item_data["quantity"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")                                  # http://127.0.0.1:5000/item
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):                                   # Retrieve all items
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):                       # Create an item
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
