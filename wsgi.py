from app import create_app
from app import db
from app.models import User, License, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'License': License}