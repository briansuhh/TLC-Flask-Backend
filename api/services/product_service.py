from api.extensions import db
from api.models.products import Product

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
