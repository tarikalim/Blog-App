from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
api = Api(version='1.0', title='Blog API', description='Blog API for Flask app',
          authorizations={
              'Bearer Auth': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              },
          },
          security='Bearer Auth', )
