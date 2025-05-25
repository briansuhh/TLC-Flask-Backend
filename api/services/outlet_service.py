from api.extensions import db
from api.models.outlets import Outlet

class OutletService:
    @staticmethod
    def create_outlet(product_id, name, price):
        new_outlet = Outlet(
            product_id=product_id,
            name=name,
            price=price
        )
        db.session.add(new_outlet)
        db.session.commit()
        return new_outlet

    @staticmethod
    def get_all_outlets():
        return Outlet.query.all()
    
    @staticmethod
    def get_outlets_by_product_id(product_id):
        if not product_id:
            raise ValueError("Product ID must be provided")
        
        return Outlet.query.filter_by(product_id=product_id).all()

    @staticmethod
    def get_outlet_by_id(outlet_id):
        return db.session.get(Outlet, outlet_id)

    @staticmethod
    def update_outlet(outlet_id, data):
        outlet = db.session.get(Outlet, outlet_id)
        if not outlet:
            return None
        
        for key, value in data.items():
            setattr(outlet, key, value)
        
        db.session.commit()
        return outlet

    @staticmethod
    def delete_outlet(outlet_id):
        outlet = db.session.get(Outlet, outlet_id)
        if not outlet:
            return False
        
        db.session.delete(outlet)
        db.session.commit()
        return True
