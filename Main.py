from flask import Flask
from src.conections.db_conexiondepelos import Connection
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.models.Models import Base

class Main:
    def __init__(self):
        self.app = Flask(__name__)

        # Configuración de la conexión
        self.connection = Connection()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.connection.connect()  
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

        self.db = SQLAlchemy(self.getApp())
        self.migrate = Migrate(self.getApp(), self.db)  # Migraciones

        # Registrar modelos y crear tablas
        self.register_models()

    def register_models(self):
        # Aquí estaba el problema de indentación
        with self.getApp().app_context():  # Abre el contexto de aplicación
            Base.metadata.create_all(self.db.engine)  # Crea las tablas

    def startApp(self):
        self.app.run(debug=True)

    def getApp(self):
        return self.app
