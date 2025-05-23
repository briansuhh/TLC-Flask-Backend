from api.extensions import db
from api.models.recipes import Recipe

class RecipeService:
    @staticmethod
    def create_recipe(product_id, item_id, quantity, isTakeout):
        new_recipe = Recipe(
            product_id=product_id,
            item_id=item_id,
            quantity=quantity,
            isTakeout=isTakeout
        )
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    @staticmethod
    def get_all_recipes():
        return Recipe.query.all()

    @staticmethod
    def get_recipe_by_product_item(product_id, item_id):
        return db.session.query(Recipe).filter_by(product_id=product_id, item_id=item_id).first()

    @staticmethod
    def update_recipe(product_id, item_id, data):
        recipe = db.session.query(Recipe).filter_by(product_id=product_id, item_id=item_id).first()
        if not recipe:
            return None
        
        for key, value in data.items():
            setattr(recipe, key, value)
        
        db.session.commit()
        return recipe

    @staticmethod
    def delete_recipe(product_id, item_id):
        recipe = db.session.query(Recipe).filter_by(product_id=product_id, item_id=item_id).first()
        if not recipe:
            return False
        
        db.session.delete(recipe)
        db.session.commit()
        return True
