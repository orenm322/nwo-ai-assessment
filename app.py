import os
from flask import Flask
from database import db, get_db_uri
from flask_jwt_extended import JWTManager
from v1.routes import bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(bp)

with app.app_context():
    db.create_all()