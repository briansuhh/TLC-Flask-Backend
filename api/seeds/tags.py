import click
from api.extensions import db
from api.models.categories import Tag
from flask.cli import with_appcontext

@click.command(name='seed_tags')
@with_appcontext
def seed_tags():
    tags = ['Masarap', 'Healthy', 'Affordable', 'Expensive']
    for tag in tags:
        db.session.add(Tag(name=tag))
    db.session.commit()
    click.echo('Tags seeded!')

def register_commands(app):
    app.cli.add_command(seed_tags)
