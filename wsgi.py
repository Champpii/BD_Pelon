from Main import Main
from flask_migrate import Migrate

main = Main()
app = main.getApp()

migrate = Migrate(app, main.db)  # Asegúrate de usar `main.db`
