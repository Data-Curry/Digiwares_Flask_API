from db import db


class WarehouseModel(db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    items = db.relationship("ItemModel", back_populates="warehouse", lazy="dynamic")
    tags = db.relationship("TagModel", back_populates="warehouse", lazy="dynamic")
