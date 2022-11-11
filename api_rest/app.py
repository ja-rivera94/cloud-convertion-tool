import os
from flask_restful import Api
from flask import Flask, jsonify
from views import SignInView, BadRequestException, LogInView,TaskView,FileView,TaskAllView, WelcomeView
from models import db
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@10.127.0.3:5432/test'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='secret-key'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(WelcomeView, '/api/status')
api.add_resource(SignInView, '/api/auth/signup')
api.add_resource(LogInView, '/api/auth/login')
api.add_resource(TaskView, '/api/tasks/<int:id_task>')
api.add_resource(FileView, '/api/files/<path:filename>')
api.add_resource(TaskView, '/api/tasks', endpoint ='/api/tasks')
api.add_resource(TaskAllView, '/api/tasks/', endpoint ='/api/tasks/')

jwt = JWTManager(app)

@app.errorhandler(BadRequestException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
