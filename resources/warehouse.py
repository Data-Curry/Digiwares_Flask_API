from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import WarehouseModel
from schemas import WarehouseSchema


blp = Blueprint("warehouses", __name__, description="operations on warehouses")


@blp.route("/warehouse/<int:warehouse_id>")                # http://127.0.0.1:5000/warehouse/<warehouse_id>
class Warehouse(MethodView):
    @blp.response(200, WarehouseSchema)
    def get(self, warehouse_id):                              # retrieve a warehouse
        warehouse = WarehouseModel.query.get_or_404(warehouse_id)
        return warehouse

    @jwt_required()
    def delete(self, warehouse_id):                           # delete a warehouse
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        warehouse = WarehouseModel.query.get_or_404(warehouse_id)
        db.session.delete(warehouse)
        db.session.commit()
        return {"message": "Warehouse deleted"}


@blp.route("/warehouse")                                      # http://127.0.0.1:5000/warehouse
class WarehouseList(MethodView):
    @jwt_required()
    @blp.response(200, WarehouseSchema(many=True))
    def get(self):                                            # Retrieve all warehouses
        return WarehouseModel.query.all()

    @jwt_required()
    @blp.arguments(WarehouseSchema)
    @blp.response(200, WarehouseSchema)
    def post(self, warehouse_data):                           # Create warehouse
        warehouse = WarehouseModel(**warehouse_data)
        try:
            db.session.add(warehouse)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Warehouse data violates the set constraints."
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the warehouse.")

        return warehouse
