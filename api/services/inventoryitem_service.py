from api.extensions import db
from api.models.inventoryitems import InventoryItem 

class InventoryItemService:
    
    @staticmethod
    def create_inventory_item(name, cost, unit, stock_warning_level, supplier_id):
        # Create a new inventory item
        new_inventory_item = InventoryItem(
            name=name,
            cost=cost,
            unit=unit,
            stock_warning_level=stock_warning_level,
            supplier_id=supplier_id
        )
        
        db.session.add(new_inventory_item)
        db.session.commit()
        return new_inventory_item
    
    @staticmethod
    def get_all_inventory_items():
        # Retrieve all inventory items and return as a list of dictionaries
        return InventoryItem.query.all()
    
    @staticmethod
    def get_inventory_item_by_id(item_id):
        # Retrieve a single inventory item by its ID
        return db.session.get(InventoryItem, item_id)
    
    @staticmethod
    def update_inventory_item(item_id, data):
        # Update an inventory item
        inventory_item = db.session.get(InventoryItem, item_id)
        if not inventory_item:
            return None
        
        for key, value in data.items():
            setattr(inventory_item, key, value)
        
        db.session.commit()
        return inventory_item
    
    @staticmethod
    def delete_inventory_item(item_id):
        # Delete an inventory item by its ID
        inventory_item = db.session.get(InventoryItem, item_id)
        if not inventory_item:
            return False
        
        db.session.delete(inventory_item)
        db.session.commit()
        return True
