from hashlib import new
from venv import create
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from flask import request, abort, send_from_directory, jsonify, Response
from models import db, User, UserSchema, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, StatementError
import os
from os import remove,path
from werkzeug.utils import secure_filename
import uuid
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import datetime

user_schema = UserSchema()
task_schema = TaskSchema()

#MP3 - ACC - OGG - WAV – WMA
ALLOWED_EXTENSIONS = set(['mp3', 'aac', 'ogg', 'wav', 'wma'])
UPLOAD_FOLDER = 'archivos/originales'
PROCESED_FOLDER = 'archivos/procesados'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'storage.json'

project_id = 'cloud-convertion-tool'
storage_client  = storage.Client(project_id)
bucket_name = 'cloud-convertion-tool-audio'
bucket = storage_client.bucket(bucket_name)



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
class TaskAllView(Resource):
    @jwt_required()
    def get(self):
        print("get_jwt_identity()")
        print(get_jwt_identity())
        identity =  str(get_jwt_identity())
        return [task_schema.dump(task) for task in Task.query.filter(Task.username == identity)]

class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        identity =  str(get_jwt_identity())
        tarea = Task.query.filter( Task.username == identity, 
                                    Task.id_task == id_task).first()
        return task_schema.dump(tarea), 200

    @jwt_required()
    def post(self):
        fileName = 'fileName'
        if fileName not in request.files:
            return {'message' : 'No file part in the request'}, 400
        file = request.files[fileName]
        if file.filename == '':
            return {'message' : 'No file selected for uploading'}, 400
        if file and allowed_file(file.filename):
            guid = str(uuid.uuid4())
            filename = guid + "-" + secure_filename(file.filename)
            filename_output = filename + "."+ str(request.form.get('newFormat'))
        
            task = Task(create_at = datetime.datetime.now(), status= "uploaded", filename_input=filename, filename_output=filename_output, username = get_jwt_identity(), guid = guid)
            db.session.add(task)
            db.session.commit()
            #destination_blob_name = filename
            destination_blob_name = UPLOAD_FOLDER + '/'+filename
#            blob = bucket.blob('file_example_WAV_2MG.wav')
            #new_blob = bucket.rename_blob(blob, destination_blob_name)
#            blob = bucket.delete_blob('901baf03-4389-466a-b37f-b1679f495246-file_example_MP3_5MG.mp3')
           
            
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(file)
            
            # Opcion 1 guardar subir y borrar
            #file.save(filename)
            #blob.upload_from_filename(filename)
            #remove(filename)
            
            return {'message' :  f"File uploaded to {destination_blob_name} in bucket {bucket_name}."}, 201
        else:
            return {'message' : 'Not Allowed file type'}, 400

    @jwt_required()
    def put(self, id_task):
        identity =  str(get_jwt_identity())
        tarea = Task.query.filter( Task.username == identity, 
                                    Task.id_task == id_task).first()
        if not "newFormat" in request.json:
            data = {
                "message": "New Format is mandatory", 
            }
            return data, 404
        else:
            if tarea is None:
                data = {
                    "message": "Task does not exists",
                    "JWT": "listo"
                }
                return data, 400
            else:
                archivo = UPLOAD_FOLDER + '/'+ tarea.filename_input
                estado = tarea.status
                mitarea = tarea.id_task
                if estado == "processed":
                    blob = bucket.blob(archivo)
                    
                    if blob.exists():
                        bucket.delete_blob(archivo)
                    else:
                        data = {
                            "message": "File 1 not found "+ archivo, 
                            "id_task": mitarea
                        }
                        return data,404

                tarea.filename_output = tarea.filename_input + "." + request.json["newFormat"]
                tarea.status = "uploaded"
                db.session.commit()

                return task_schema.dump(tarea), 200
        
    @jwt_required()
    def delete(self,id_task):
        identity =  str(get_jwt_identity())
        tarea = Task.query.filter(Task.username == identity,
                                 Task.id_task == id_task).first()
        if tarea is None:
            data = {
                "message": "No encontrado", 
                "JWT": "listo"
            }
            return data,404
        else:
            archivo = UPLOAD_FOLDER + '/'+ tarea.filename_input
            archivo2 =PROCESED_FOLDER + '/'+ tarea.filename_output
            estado = tarea.status
            mitarea = tarea.id_task
            if estado == "processed":
                blob = bucket.blob(archivo)
                if blob.exists(archivo):
                    blob2 = bucket.blob(archivo)
                    if blob2.exists(archivo2):
                        bucket.delete_blob(archivo)
                        bucket.delete_blob(archivo2)
                        if not  blob.exists(archivo) and not blob2.exists(archivo2):
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
        blob = bucket.get_blob('archivos/'+filename)   
        if blob :
            content_type = None
            try:
                content_type = blob.content_type
            except:
                pass
            file = blob.download_as_string()
            print(type(file), "downloaded type")
            return Response(file,  mimetype=content_type)
        data = {
                    "message":"File not found ", 
                    "filename": filename
                }
        return data,404

class WelcomeView(Resource):
    def get(self):
        return jsonify({'status': 'api working'})