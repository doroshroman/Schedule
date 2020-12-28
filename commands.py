import click
import sys
from flask.cli import with_appcontext
from app import db
from app.models import Administrator


@click.group()
def cli():
    pass


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    click.echo('Tables have been created')

@click.command(name='create_admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(username, email, password):
    admin = Administrator.query.filter_by(username=username, email=email).first()
    if admin:
        click.echo('Admin already exists')
        return 
    admin = Administrator(username=username, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin has been created')


cli.add_command(create_tables)
cli.add_command(create_admin)

if __name__ == "__main__":
    cli()