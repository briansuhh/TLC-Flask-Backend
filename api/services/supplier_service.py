from api.extensions import db
from api.models.suppliers import Supplier

class SupplierService:
    @staticmethod
    def create_supplier(name, email, phone, country_code):
        new_supplier = Supplier(
            name=name,
            email=email,
            phone=phone,
            country_code=country_code
        )
        db.session.add(new_supplier)
        db.session.commit()
        return new_supplier

    @staticmethod
    def get_all_suppliers():
        return Supplier.query.all()

    @staticmethod
    def get_supplier_by_id(supplier_id):
        return db.session.get(Supplier, supplier_id)

    @staticmethod
    def update_supplier(supplier_id, data):
        supplier = db.session.get(Supplier, supplier_id)
        if not supplier:
            return None
        
        for key, value in data.items():
            setattr(supplier, key, value)
        
        db.session.commit()
        return supplier

    @staticmethod
    def delete_supplier(supplier_id):
        supplier = db.session.get(Supplier, supplier_id)
        if not supplier:
            return False
        
        db.session.delete(supplier)
        db.session.commit()
        return True
