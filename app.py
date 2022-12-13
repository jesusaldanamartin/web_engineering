import pandas
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request,url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from sqlalchemy.sql import exists, select
from flask_bootstrap import Bootstrap
from tkinter import messagebox




app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
       return f"<User id={self.id} name={self.name} email={self.email} password={self.password} status={self.status} date={self.date}>"

class Tareas(db.Model):
    __tablename__ = 'Tareas'
    id = db.Column(db.String(100), primary_key=True)
    descripcionTarea = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(120), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task id={self.id} descipcionTarea={self.descripcionTarea} tipo={self.tipo} date={self.date}>"

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

class Robots(db.Model):
    __tablename__ = 'Robots'
    id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    id_Tareas = db.Column(db.String(100), db.ForeignKey(Tareas.id), primary_key= True)
    tipoTarea = db.Column(db.String(150), db.ForeignKey(Tareas.descripcionTarea), primary_key= True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Robot id={self.id} name={self.name} id_Tarea={self.id_Tareas} tipoTarea={self.tipoTarea} date={self.date}>"



def inserts():
    usr = Users(id=0, name="admin", email="email_admin@example.com", password="admin", status="admin")
    usr2 = Users(id=10, name="person2", email="email_medico@example.com", password="67890", status="medico")
    #usr3 = Users(id=20, name="person2", email="email_tecnico@example.com", password="67890", status="admin")
    #usr4 = Users(id=30, name="person2", email="email_medico2@example.com", password="67890", status="medico")

    tarea1 = Tareas(id = 0, descripcionTarea = "Limpieza pasillo", tipo = "Limpieza")
    tarea2 = Tareas(id = 1, descripcionTarea = "Transporte Medicamentos", tipo = "Transporte" )

    robot1 = Robots(id = 0, name = "Robot1", id_Tareas = 0, tipoTarea = "Limpieza pasillo")
    robot2 = Robots(id = 1, name = "Robot2", id_Tareas = 1, tipoTarea = "Transporte de Medicamentos")

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
    

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = db.session.query(exists().where(Users.name == username)).scalar()
        password_exists = db.session.query(exists().where(Users.password == password)).scalar()
        usuario_registrado = db.session.query(Users).where(Users.name == username, Users.password == password).one()
  
        if (user_exists and password_exists):
            if (str(usuario_registrado.status) == "admin"):
                return redirect('/admin')
            else:
                return redirect('/doctor')         
    else:
        return render_template('log.jinja')

@app.route("/admin")
def admin():

    usuarios_db = db.session.query(Users).all()
    tareas_db = db.session.query(Tareas).all()
    robots_db = db.session.query(Robots).all()

    #for user in usuarios_db: print(user.name)
    #for task in tareas_db: print(task.name)
    #for robot in robots_db: print(robot.name)

    return render_template('template_tecnico.jinja', usuarios = usuarios_db, tareas = tareas_db, robots = robots_db)

@app.route("/doctor")
def doctor():
    robots_db = db.session.query(Robots).all()
    tareas_db = db.session.query(Tareas).all()

    #for task in tareas_db: print(task.name)
    #for robot in robots_db: print(robot.name)

    return render_template('template_medico.jinja', usuarios = robots_db, tareas = tareas_db)

@app.route("/doctor/robot1")
def robot():
    return render_template('template_robot.jinja')

@app.route("/admin/formularioTareas", methods=["GET","POST"])
def tarea():

    if request.method == 'POST':
        id_tarea= request.form['id']
        descripcion_tarea= request.form['descripcionTarea']
        tipo_tarea = request.form['tipo']

        tarea_exists = db.session.query(exists().where(Tareas.id == id_tarea)).scalar()
        if (tarea_exists):
            messagebox.showinfo(message="La tarea ya existe, prueba otro ID", title="ERROR CREANDO TAREA")
            return render_template('formulario_tecnico_tareas.jinja')

        else: 
            tarea = Tareas(id = id_tarea, descripcionTarea = descripcion_tarea, tipo = tipo_tarea)
            db.session.add(tarea)
            db.session.commit()
            return render_template('formulario_tecnico_tareas.jinja')
        
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