from src.models.models import DimFecha, DimCategoria, DimProducto, FactVentas

class AppInitializer:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.register_models()

    def register_models(self):
        # Crear las tablas en la base de datos si no existen
        with self.app.app_context():
            self.db.create_all()
