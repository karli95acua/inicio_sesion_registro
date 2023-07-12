from flask import session, render_template, redirect, request, flash
from flask_bcrypt import Bcrypt
from app_inicio_sesion import app
from app_inicio_sesion.models.model_users import User

bcrypt = Bcrypt(app)

@app.route('/', methods = ['GET'])
def deploy_login_registration():
    return render_template('login_registration.html')

@app.route('/create/user', methods = ['POST'])
def new_user():
    data = {
        **request.form

    }

    if User.validate_registration(data) == False:
        return redirect('/')
    else:
        password_encriptado = bcrypt.generate_password_hash(data["password"])
        data["password"] = password_encriptado
        id_user = User.create_one(data)
        session["first_name"] = data["first_name"]
        session["last_name"] = data["last_name"]
        session["id_user"] = id_user
        return redirect("/dashboard")

@app.route('/dashboard', methods = ['GET'])
def deploy_dashboard():
    if "first_name" not in session:
        return redirect("/")
    else:
        return render_template("dashboard.html")

@app.route('/login', methods= ['POST'])
def process_login():
    data = {
        "email" : request.form["email_login"]
    }
    user = User.get_one_by_email(data)

    if user == None:
        flash("Email inválido.", "error_email_login")
        return redirect("/")
    else:
        if not bcrypt.check_password_hash(user.password, request.form["password_login"]):
            flash("Credenciales incorrectas.", "error_password_login")
            return redirect('/')
        else:
            session["first_name"] = user.first_name
            session["last_name"] = user.last_name
            session["id_user"] = user.id
            return redirect("/dashboard")

@app.route('/logout', methods= ['POST'])
def process_logout():
    session.clear()
    return redirect('/')