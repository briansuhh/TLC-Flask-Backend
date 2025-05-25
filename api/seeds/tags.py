import click
from api.extensions import db
from api.models.tags import Tag
from flask.cli import with_appcontext

@click.command(name='seed_tags')
@with_appcontext
def seed_tags():
    """Seed the database with initial Tag data."""
    
    tags = [
        Tag(name="Masarap"),
        Tag(name="Healthy"),
        Tag(name="Affordable"),
        Tag(name="Expensive")
    ]
    
    # Bulk save the Tag objects to the database
    db.session.bulk_save_objects(tags)
    db.session.commit()
    click.echo('Tags seeded!')

def register_commands(app):
    app.cli.add_command(seed_tags)
