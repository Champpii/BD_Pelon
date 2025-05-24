# wsgi.py
from Main import Main

main_instance = Main()
app = main_instance.getApp()  # Esto es lo que Flask espera: una variable llamada 'app'
