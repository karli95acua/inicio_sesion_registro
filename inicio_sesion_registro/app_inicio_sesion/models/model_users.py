from app_inicio_sesion.config.mysqlconnection import connectToMySQL
from app_inicio_sesion import BASE_DATOS, EMAIL_REGEX, NAME_REGEX
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create_one(cls, data):
        query = """
                INSERT INTO users(first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        return resultado
    
    @classmethod
    def get_one_by_email(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        if len(resultado) == 0:
            return None
        else:
            return User(resultado[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            is_valid = False
            flash("Tu nombre debe contener al menos 2 carácteres.", "error_first_name")
        if not NAME_REGEX.match(data["first_name"]):
            is_valid = False
            flash("Por favor, proporciona un nombre válido (solo letras).", "error_first_name")
        if len(data["last_name"]) < 2:
            is_valid = False
            flash("Tu nombre debe contener al menos 2 carácteres.", "error_last_name")
        if not NAME_REGEX.match(data["last_name"]):
            is_valid = False
            flash("Por favor, proporciona un apellido válido (solo letras).", "error_last_name")
        if not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Por favor, proporciona un email válido.", "error_email")
        if len(data["password"]) < 8:
            is_valid = False
            flash("Tu password debe contener al menos 8 carácteres.", "error_password")
        if data["password"] != data["password_confirmation"]:
            is_valid = False
            flash("Tus password no coinciden.", "error_password")
        return is_valid