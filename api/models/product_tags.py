from api.extensions import db

class ProductTag(db.Model):
    __tablename__ = 'product_tags'

    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)

    product = db.relationship('Product', back_populates='tags')
    tag = db.relationship('Tag', back_populates='products')
