from hashlib import new
from venv import create
from flask import request, abort
from models import db, User, UserSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, StatementError
import datetime

user_schema = UserSchema()

class BadRequestException(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class SignInView(Resource):
    
    def post(self):
        try:
            password1 = request.json["password1"]
            password2 = request.json["password2"]
            if(password1 != password2):
                raise Exception("Password does match with confirmation password")

            new_user = User(username=request.json["username"], password = password1, email=request.json["email"], create_at = datetime.datetime.now())
            db.session.add(new_user)
            db.session.commit()
            
            return {"message":"Usuario creado correctamente"}, 201

        except Exception as ex:
            db.session.rollback()
            raise BadRequestException(format(ex))

