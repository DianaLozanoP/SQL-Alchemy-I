"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS WILL GO BELOW HERE


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.String(),
                          nullable=False,
                          default='https://www.freeiconspng.com/img/7563')

    def update_information(self, first_name, last_name, image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    @classmethod
    def delete_user(cls, id):
        """Delete the user with that ID"""
        return cls.query.filter(User.id == id).delete()
