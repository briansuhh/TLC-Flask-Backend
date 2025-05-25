import click
from api.extensions import db
from api.models.products import Product
from flask.cli import with_appcontext

@click.command("seed_products")
@with_appcontext
def seed_products():
    """Seed the database with initial data."""

    products = [
    Product(name="Beef Tapa", category_id=1, variant_group_id="BEEF-TAPA", sku="SKU-0001"),
    Product(name="Bacon", category_id=1, variant_group_id="BACON", sku="SKU-0002"),
    Product(name="K-SPAM", category_id=1, variant_group_id="K-SPAM", sku="SKU-0003"),
    Product(name="Tocino", category_id=1, variant_group_id="TOCINO", sku="SKU-0004"),
    Product(name="Spanish Sardines", category_id=1, variant_group_id="SARDINES-SP", sku="SKU-0005"),
    Product(name="Boneless Bangus", category_id=1, variant_group_id="BANGUS-BONELESS", sku="SKU-0006"),
    Product(name="Hungarian Sausage", category_id=1, variant_group_id="SAUSAGE-HUNG", sku="SKU-0007"),
    Product(name="Corned Beef", category_id=1, variant_group_id="BEEF-CORNED", sku="SKU-0008"),
    Product(name="Homemade Longganisa", category_id=1, variant_group_id="LONGGANISA-HM", sku="SKU-0009"),
    Product(name="TLC Cheesecake Carousel", category_id=2, variant_group_id="CHEESECAKE-TLC", sku="SKU-0010"),
    Product(name="Basque Burnt Cheesecake", category_id=2, variant_group_id="CHEESECAKE-BB", sku="SKU-0011"),
    Product(name="Dark Chocolate Blackout", category_id=2, variant_group_id="CAKE-BLKOUT", sku="SKU-0012"),
    Product(name="Red Velvet Cake", category_id=2, variant_group_id="CAKE-RV", sku="SKU-0013"),
    Product(name="Beef Tapa", category_id=2, variant_group_id="BEEF-TAPA", sku="SKU-0014"),
    Product(name="Sausage Tomato Cream Pasta", category_id=2, variant_group_id="PASTA-STC", sku="SKU-0015"),
    Product(name="Iced Authentic Vietnamese Drinks", category_id=2, variant_group_id="DRINKS-VIET", sku="SKU-0016"),
    Product(name="Iced Dark Chocolate Mocha", category_id=2, variant_group_id="MOCHA-DARK", sku="SKU-0017"),
    Product(name="Signature Iced Tea", category_id=2, variant_group_id="TEA-SIG", sku="SKU-0018"),
    Product(name="TLC Cheesecake Carousel", category_id=3, variant_group_id="CHEESECAKE-TLC", sku="SKU-0019"),
    Product(name="Trio Cake", category_id=3, variant_group_id="CAKE-TRIO", sku="SKU-0020"),
    Product(name="Basque Burnt Cheesecake", category_id=3, variant_group_id="CHEESECAKE-BB", sku="SKU-0021"),
    Product(name="Red Velvet Cake", category_id=3, variant_group_id="CAKE-RV", sku="SKU-0022"),
    Product(name="Dark Chocolate Blackout", category_id=3, variant_group_id="CAKE-BLKOUT", sku="SKU-0023"),
    Product(name="Ube Burnt Cheesecake", category_id=3, variant_group_id="CHEESECAKE-UBE", sku="SKU-0024"),
    Product(name="Carrot Cake", category_id=3, variant_group_id="CAKE-CARROT", sku="SKU-0025"),
    Product(name="Double Chocolate Cheesecake", category_id=3, variant_group_id="CHEESECAKE-DCC", sku="SKU-0026"),
    Product(name="Blueberry Cheesecake", category_id=3, variant_group_id="CHEESECAKE-BLUE", sku="SKU-0027"),
    Product(name="Mango Cheesecake Slice", category_id=4, variant_group_id="SLICE-MANGO", sku="SKU-0028"),
    Product(name="Blueberry Cheesecake Slice", category_id=4, variant_group_id="SLICE-BLUE", sku="SKU-0029"),
    Product(name="Basque Burnt Cheesecake Slice", category_id=4, variant_group_id="SLICE-BB", sku="SKU-0030"),
    Product(name="Dark Chocolate Blackout Cake Slice", category_id=4, variant_group_id="SLICE-BLKOUT", sku="SKU-0031"),
    Product(name="Red Velvet Cake Slice", category_id=4, variant_group_id="SLICE-RV", sku="SKU-0032"),
    Product(name="Carrot Cake Slice", category_id=4, variant_group_id="SLICE-CARROT", sku="SKU-0033"),
    Product(name="Strawberry Cheesecake Slice", category_id=4, variant_group_id="SLICE-STRAW", sku="SKU-0034"),
    Product(name="Lemon Cheesecake Slice", category_id=4, variant_group_id="SLICE-LEMON", sku="SKU-0035"),
    Product(name="Iced Americano", category_id=5, variant_group_id="COFFEE-AMER", sku="SKU-0036"),
    Product(name="Iced Cafe Latte", category_id=5, variant_group_id="COFFEE-LATTE", sku="SKU-0037"),
    Product(name="Iced Cappuccino", category_id=5, variant_group_id="COFFEE-CAPPU", sku="SKU-0038"),
    Product(name="Iced Dark Chocolate Mocha", category_id=5, variant_group_id="MOCHA-DARK", sku="SKU-0039"),
    Product(name="Iced White Choco Mocha", category_id=5, variant_group_id="MOCHA-WHITE", sku="SKU-0040"),
    Product(name="Iced Caramel Latte", category_id=5, variant_group_id="LATTE-CARAMEL", sku="SKU-0041"),
    Product(name="Iced Vanilla Latte", category_id=5, variant_group_id="LATTE-VANILLA", sku="SKU-0042"),
    Product(name="Iced Hazelnut Latte", category_id=5, variant_group_id="LATTE-HAZELNUT", sku="SKU-0043"),
    Product(name="Iced Matcha Latte", category_id=5, variant_group_id="LATTE-MATCHA", sku="SKU-0044"),
    Product(name="Signature Iced Tea", category_id=5, variant_group_id="TEA-SIG", sku="SKU-0045")
]
    
    db.session.bulk_save_objects(products)
    db.session.commit()
    print("Products seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_products)