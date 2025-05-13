from flask_sqlalchemy import SQLAlchemy

# Assuming db is already initialized in your main app or a shared models file
# If not, you would initialize it here: db = SQLAlchemy()
# For this project, db is initialized in models/user.py and then imported.
from .user import db

class SiteConfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<SiteConfiguration {self.key}="{self.value}">'
