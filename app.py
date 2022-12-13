import pandas
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request,url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from sqlalchemy.sql import exists, select
from flask_bootstrap import Bootstrap



app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.status

class Tareas(db.Model):
    __tablename__ = 'Tareas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return self.id

class Admin(db.Model):
    __tablename__ = 'Administrators'
    admin = db.Column(db.String(100), db.ForeignKey(Users.id), primary_key= True)

    def __repr__(self):
        return '<admin %r>' % self.admin

class Doctor(db.Model):
    __tablename__ = 'Doctors'
    doctor = db.Column(db.String(100), db.ForeignKey(Users.id), primary_key= True)

    def __repr__(self):
        return '<doctor %r>' % self.doctor

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4,max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=50)])
    remember = BooleanField('Remember me')

class Robots(db.Model):
    __tablename__ = 'Robots'
    id_Tareas = db.Column(db.String(100), db.ForeignKey(Tareas.id), primary_key= True)
    tipoTarea = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TipoTarea %r>' % self.tipoTarea


def inserts():
    usr = Users(id=0, name="admin", email="email_admin@example.com", password="admin", status="admin")
    usr2 = Users(id=10, name="person2", email="email_medico@example.com", password="67890", status="medico")
    #usr3 = Users(id=20, name="person2", email="email_tecnico@example.com", password="67890", status="admin")
    #usr4 = Users(id=30, name="person2", email="email_medico2@example.com", password="67890", status="medico")

    tarea1 = Tareas(id = 0, name = "Robot1", tipo = "Limpieza")
    tarea2 = Tareas(id = 1, name = "Robot2", tipo = "Transporte" )

    robot1 = Robots(id_Tareas = 0, tipoTarea = "Limpieza de Suelo", name = "Robot1")
    robot2 = Robots(id_Tareas = 1, tipoTarea = "Transporte de Medicamentos", name = "Robot2")

    db.session.add(usr)
    db.session.commit()
    db.session.add(usr2)
    db.session.commit()

    db.session.add(tarea1)
    db.session.commit()
    db.session.add(tarea2)
    db.session.commit()

    db.session.add(robot1)
    db.session.commit()
    db.session.add(robot2)
    db.session.commit()
    

@app.route("/form")
def form_flask():
    form = LoginForm()
    return render_template('home.html', form=form)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        status = 'admin'

        user_exists = db.session.query(exists().where(Users.name == username)).scalar()
        password_exists = db.session.query(exists().where(Users.password == password)).scalar()
        #is_admin = db.session.query(exists().where(Users.status == status)).scalar()

        person = select(Users).where(Users.name == username, Users.password == password)
        get_status = db.session.execute(person).all()
        
        print(person)
        print(str(get_status[0][0]))
        print(user_exists)
        print(password_exists)
        if (user_exists and password_exists):
            if (str(get_status[0][0]) == "admin"):
                return redirect('/admin')
            else:
                return redirect('/doctor')
                  
    else:
        return render_template('log.jinja')

@app.route("/admin")
def admin():
    return render_template('template_tecnico.jinja')

@app.route("/doctor")
def doctor():
    return render_template('template_medico.jinja')

@app.route("/doctor/robot1")
def robot():
    return render_template('template_robot.jinja')


@app.route("/admin/formularioTareas")
def tarea():
    return render_template('formulario_tecnico_tareas.jinja')


@app.route("/admin/formularioUsuarios")
def usuario():
    return render_template('formulario_tecnico_usuario.jinja')

if __name__ == "__main__":
    app.app_context().push()
    db.drop_all()
    db.create_all()
    inserts()
    app.run(debug=True)