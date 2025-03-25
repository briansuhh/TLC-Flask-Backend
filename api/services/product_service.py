from api.extensions import db
from api.models.products import Product
from api.models.tags import Tag
from api.models.product_tags import ProductTag

class ProductService:
    @staticmethod
    def create_product(name, variant_group_id, sku, category_id):
        new_product = Product(
            name=name,
            variant_group_id=variant_group_id,
            sku=sku,
            category_id=category_id
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def get_all_products():
        return [product.to_dict() for product in Product.query.all()]

    @staticmethod
    def get_product_by_id(product_id):
        return db.session.get(Product, product_id)

    @staticmethod
    def update_product(product_id, data):
        product = db.session.get(Product, product_id)
        if not product:
            return None
        
        for key, value in data.items():
            setattr(product, key, value)
        
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = db.session.get(Product, product_id)
        if not product:
            return False
        
        db.session.delete(product)
        db.session.commit()
        return True
    
    @staticmethod
    def add_tag_to_product(product_id, tag_id):
        """Attach a tag to a product"""
        product = db.session.get(Product, product_id)
        tag = db.session.get(Tag, tag_id)

        if not product or not tag:
            return False

        new_product_tag = ProductTag(product_id=product_id, tag_id=tag_id)
        db.session.add(new_product_tag)
        db.session.commit()
        return True

    @staticmethod
    def get_product_tags(product_id):
        """Retrieve all tags associated with a product"""
        product_tags = ProductTag.query.filter_by(product_id=product_id).all()
        return [{"tag_id": pt.tag_id, "name": pt.tag.name} for pt in product_tags]

    @staticmethod 
    def update_product_tag(product_id, tag_id, data):
        """Update a product-tag association"""
        product_tag = db.session.query(ProductTag).filter_by(product_id=product_id, tag_id=tag_id).first()
        if not product_tag:
            return None

        for key, value in data.items():
            setattr(product_tag, key, value)

        db.session.commit()
        return product_tag

    @staticmethod
    def remove_tag_from_product(product_id, tag_id):
        """Remove a tag from a product"""
        product_tag = ProductTag.query.filter_by(product_id=product_id, tag_id=tag_id).first()
        if not product_tag:
            return False

        db.session.delete(product_tag)
        db.session.commit()
        return True