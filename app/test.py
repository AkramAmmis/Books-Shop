from models.model import Book
from . import app
with app.app_context():
    Books = Book.query.all()