from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    create_at = db.Column(db.DateTime)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = User
         include_relationships = True
         load_instance = True