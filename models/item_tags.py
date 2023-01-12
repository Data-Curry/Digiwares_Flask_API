from db import db


# This defines the secondary table used in a many-to-many relationship
class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))  # One side of the relationship
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))    # The other side of the relationship
