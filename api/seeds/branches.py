import click
from api.extensions import db
from api.models.branches import Branch
from flask.cli import with_appcontext
from datetime import datetime, UTC

@click.command("seed_branches")
@with_appcontext
def seed_branches():
    """Seed the database with initial branches data."""

    branches = [
        Branch(
            name="TLC Mandaluyong",
            address="124 Mandaluyong mandaluyon mandaluyong"
        ),
        Branch(
            name="TLC Manila",
            address="124 Manila manila manila"
        ),
        Branch(
            name="TLC San Juan",
            address="124 Sanjuan sanjuan sanjuan"
        )
    ]

    db.session.bulk_save_objects(branches)
    db.session.commit()
    print("Branches seeded successfully!")

# Register CLI command with Flask
def register_commands(app):
    app.cli.add_command(seed_branches)
