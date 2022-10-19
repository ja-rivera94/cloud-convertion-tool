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
       
class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime)
    status = db.Column(db.String(10))
    filename_input = db.Column(db.String(255))
    filename_output = db.Column(db.String(255))
    username = db.Column(db.String(50))
    guid =  db.Column(db.String(255))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = User
         include_relationships = True
         load_instance = True

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Task
         include_relationships = True
         load_instance = True