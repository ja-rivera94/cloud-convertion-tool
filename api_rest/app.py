import os
from flask_restful import Api
from flask import Flask, jsonify
from views import SignInView, BadRequestException, LogInView
from models import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='secret-key'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(SignInView, '/auth/signup')
api.add_resource(LogInView, '/auth/login')

jwt = JWTManager(app)

@app.route('/')
def welcome():
    return jsonify({'status': 'api working'})

@app.errorhandler(BadRequestException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)