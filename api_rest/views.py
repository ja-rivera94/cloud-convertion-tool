from hashlib import new
from venv import create
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from flask import request, abort, send_from_directory
from models import db, User, UserSchema, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, StatementError
from os import remove,path

import datetime

user_schema = UserSchema()
task_schema = TaskSchema()

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
        rv['code'] = self.status_code
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

class LogInView(Resource):

    def post(self):
        try:
            user = User.query.filter(User.username == request.json["username"],
                                 User.password == request.json["password"]).first()
            if user is None:
                raise Exception("Username or password incorrect")
            else:
                token_de_acceso = create_access_token(identity=user.id)

                data = {
                    "message": "Authenticaion succed", 
                    "JWT": token_de_acceso
                }
            return data
        except Exception as ex:
            db.session.rollback()
            raise BadRequestException(format(ex))
        
class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        usuario = User.query.filter(User.id == get_jwt_identity()).first()
        tarea = Task.query.filter( Task.username == usuario.username, 
                                    Task.id_task == id_task).first()
        return task_schema.dumps(tarea)

    @jwt_required()
    def delete(self,id_task):
        miusuario = "oscar"
        mipath = "archivos"
        tarea = Task.query.filter(Task.username == miusuario,
                                 Task.id_task == id_task).first()
        
        if tarea is None:
            data = {
                "message": "No encontrado", 
                "JWT": "listo"
            }
            return data,404
        else:
            archivo = path.join(mipath, tarea.filename_input)
            archivo2 = path.join(mipath, tarea.filename_output)
            estado = tarea.status
            mitarea = tarea.id_task
            if estado == "processed":
                if path.exists(archivo):
                    if path.exists(archivo2):
                        remove(archivo)
                        remove(archivo2)
                        if not path.exists(archivo) and not path.exists(archivo2):
                            data = {
                                "message": "Deleted files "+archivo + " " + archivo2, 
                                "id_task": mitarea
                            }
                        else:
                            data = {
                                "message": "Files could not be deleted "+archivo + " " + archivo2, 
                                "id_task": mitarea
                            }
                            return data,404
                    else:
                        data = {
                            "message": "File 2 not found: "+ archivo2, 
                            "id_task": mitarea
                        }
                        return data,404
                else:
                    data = {
                        "message": "File 1 not found "+ archivo, 
                        "id_task": mitarea
                    }
                    return data,404
            else:
                data = {
                        "message": "The files cannot be deleted because the status is not processed", 
                        "id_task": mitarea
                    }
                return data,404
            
        return data

class FileView(Resource):    
    @jwt_required()
    def get(self,filename):    
        mipath = "archivos"
        if path.isfile(path.join(mipath, filename)):
            return send_from_directory(mipath, filename, as_attachment=True)
        data = {
                    "message":"File not found ", 
                    "filename": filename
                }
        return data,404
