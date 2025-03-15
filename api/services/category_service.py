from api.extensions import db
from api.models.categories import Category

class CategoryService:
    @staticmethod
    def create_category(name):
        new_category = Category(
            name=name
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        return db.session.get(Category, category_id)
    
    @staticmethod
    def update_category(category_id, data):
        category = db.session.get(Category, category_id)
        if not category:
            return None
        
        for key, value in data.items():
            setattr(category, key, value)
        
        db.session.commit()
        return category
    
    @staticmethod
    def delete_category(category_id):
        category = db.session.get(Category, category_id)
        if not category:
            return False
        
        db.session.delete(category)
        db.session.commit()
        return True
    