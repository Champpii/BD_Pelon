# Main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.conections.db_conection import Connection
from src.config.app_initializer import AppInitializer

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.connection = Connection()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.connection.connect()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy(self.app)
        self.migrate = Migrate(self.app, self.db)

        with self.app.app_context():
            from src.models.Models import Base
            Base.metadata.create_all(self.db.engine)

        self.app_initializer = AppInitializer(self.app, self.db)

    def getApp(self):
        return self.app

    def getDb(self):
        return self.db
