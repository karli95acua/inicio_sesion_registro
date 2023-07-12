from app_inicio_sesion import app
from app_inicio_sesion.controllers import controller_users

if __name__ == "__main__":
    app.run(debug=True, port = 5020)