from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TagModel, WarehouseModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/warehouse/<int:warehouse_id>/tag")
class TagsInWarehouse(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, warehouse_id):                                      # Retrieve all tags in a warehouse
        warehouse = WarehouseModel.query.get_or_404(warehouse_id)

        return warehouse.tags.all()                                   # lazy="dynamic" means 'tags' is a query

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, warehouse_id):                           # Create tag
        tag = TagModel(**tag_data, warehouse_id=warehouse_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
            )

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):                                 # Link a tag to an item
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.warehouse_id != tag.warehouse_id:
            abort(400, message="Make sure the item and tag belong to the same warehouse before linking.")

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):               # Unlink a tag from an item
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):                            # Retrieve a tag
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description="Deletes the tag if no item is tagged with it.",
        example={"message": "Tag deleted."}
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted."
    )
    def delete(self, tag_id):                         # Delete a tag
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again."
        )
