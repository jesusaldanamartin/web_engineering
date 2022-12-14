from tkinter import messagebox
import pandas
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request,url_for, flash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from sqlalchemy.sql import exists, select
from sqlalchemy import exc
from flask_bootstrap import Bootstrap


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
    tipo = db.Column(db.String(120), nullable=False)
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
    id = db.Column(db.String(150), nullable=False, primary_key= True)
    name = db.Column(db.String(150), nullable=False)
    id_Tareas = db.Column(db.String(100), db.ForeignKey(Tareas.id))
    tipoTarea = db.Column(db.String(150), db.ForeignKey(Tareas.descripcionTarea))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Robot id={self.id} name={self.name} id_Tarea={self.id_Tareas} tipoTarea={self.tipoTarea} date={self.date}>"

class Tabla_Medico(db.Model):
    __tablename__ = 'Tabla medico'
    id_robot = db.Column(db.String(150), nullable=False, primary_key= True)
    name_robot = db.Column(db.String(150))   #, db.ForeignKey(Robots.name))
    id_Tareas = db.Column(db.String(100))    #, db.ForeignKey(Tareas.id))
    realizando_tarea = db.Column(db.String(150),nullable=False )
    tipoTarea = db.Column(db.String(150))  #,db.ForeignKey(Tareas.descripcionTarea))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TablaMedica id={self.id_robot} name={self.name_robot} id_Tarea={self.id_Tareas} realizandoTarea={self.realizando_tarea} date={self.date}>"



def inserts():
    usr = Users(id=0, name="admin", email="email_admin@example.com", password="admin", status="admin")
    usr2 = Users(id=10, name="person2", email="email_medico@example.com", password="67890", status="medico")
    #usr3 = Users(id=20, name="person2", email="email_tecnico@example.com", password="67890", status="admin")
    #usr4 = Users(id=30, name="person2", email="email_medico2@example.com", password="67890", status="medico")

    tarea1 = Tareas(id = 0, descripcionTarea = "Limpieza pasillo", tipo = "Limpieza")
    tarea2 = Tareas(id = 1, descripcionTarea = "Transporte Medicamentos", tipo = "Transporte" )

    robot1 = Robots(id = 0, name = "Robot1", id_Tareas = 0, tipoTarea = "Limpieza pasillo")
    robot2 = Robots(id = 1, name = "Robot2", id_Tareas = 1, tipoTarea = "Transporte de Medicamentos")

    accion1 = Tabla_Medico(id_robot=0, name_robot="Robot1", id_Tareas=1, realizando_tarea="Ocupado",tipoTarea="Limpieza pasillo" )
    accion2 = Tabla_Medico(id_robot=1, name_robot="Robot2", id_Tareas=1, realizando_tarea="Disponible",tipoTarea="..." )

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

    db.session.add(accion1)
    db.session.commit()
    db.session.add(accion2)
    db.session.commit()


#* --- RUTAS DE FLASK ---
    

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        try:
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
            

        except exc.NoResultFound:
            flash('Credenciales incorrectas.')
            
            return render_template('log.jinja') 
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

@app.route("/doctor", methods=["GET", "POST"])
def doctor():
    robots_db = db.session.query(Robots).all()
    tareas_db = db.session.query(Tareas).all()
    accion_db = db.session.query(Tabla_Medico).all()

    #for task in tareas_db: print(task.name)
    #for robot in robots_db: print(robot.name)

    return render_template('template_medico.jinja', robots = robots_db, tareas = tareas_db, acciones=accion_db)

@app.route("/deleteTarea/<id_t>")
def delete_tarea(id_t):

    tarea_exists = db.session.query(Tareas).get(id_t)
    db.session.delete(tarea_exists)
    db.session.commit()

    return redirect(url_for('admin'))

@app.route("/deleteUsuario/<id_u>")
def delete_usuario(id_u):

    usuario = db.session.query(Users).get(id_u)
    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for('admin'))

@app.route("/deleteRobot/<id_t>")
def delete_robot(id_t):

    robot = db.session.query(Robots).get(id_t)
    db.session.delete(robot)
    db.session.commit()

    return redirect(url_for('admin'))

@app.route("/doctor/<robot_name>")
def robot(robot_name):
    return render_template('template_robot.jinja', name=robot_name)

@app.route("/admin/formularioTareas", methods=["GET","POST"])
def tarea():
    tareaNula = Tareas()
    if request.method == 'POST':
        id_tarea = request.form['id']
        descripcion_tarea= request.form['descripcionTarea']
        tipo_tarea = request.form['tipo']
        tarea_exists = db.session.query(exists().where(Tareas.id == id_tarea)).scalar()

        if (tarea_exists):
            messagebox.showinfo(message="La tarea ya existe o faltan campos por rellenar", title="ERROR CREANDO TAREA")
            return render_template('formulario_tecnico_tareas.jinja')

        else: 
            tarea = Tareas(id = id_tarea, descripcionTarea = descripcion_tarea, tipo = tipo_tarea)
            db.session.add(tarea)
            db.session.commit()
            return render_template('formulario_tecnico_tareas.jinja', tabla=tareaNula)
        
    return render_template('formulario_tecnico_tareas.jinja', tabla = tareaNula)

@app.route("/admin/formularioUsuarios" , methods=["GET","POST"])
def usuario():
    if request.method == 'POST':

        id_usuario = request.form['id']
        name_usuario = request.form['name']
        email_usuario = request.form['email']
        password_usuario = request.form['password']
        status_usuario = request.form['status']
        


        id_exists = db.session.query(exists().where(Users.id == id_usuario)).scalar()
        if (id_exists):
            messagebox.showinfo(message="El usuario ya existe, prueba otro ID", title="ERROR CREANDO USUARIO")
            return render_template('formulario_tecnico_usuario.jinja')

        else:
            usuario = Users(id = id_usuario, name = name_usuario, email = email_usuario, password = password_usuario, status = status_usuario)
            db.session.add(usuario)
            db.session.commit()
            
            return render_template('formulario_tecnico_usuario.jinja')
        
    return render_template('formulario_tecnico_usuario.jinja')


@app.route("/admin/formularioRobots", methods=["GET","POST"])
def robot_tecnico():

    if request.method == 'POST':
        id_robot = request.form['id']
        name_robot=  request.form['name']
        id_tarea= request.form['id_Tareas']
        tipo_tarea = request.form['tipoTarea']

        robot_exists = db.session.query(exists().where(Robots.id == id_robot)).scalar()
        tarea_exists = db.session.query(exists().where(Tareas.id == id_tarea)).scalar()
        tarea_tipo_exists = db.session.query(exists().where(Tareas.descripcionTarea == tipo_tarea)).scalar()

        if (robot_exists):
            messagebox.showinfo(message="Este robot ya existe, prueba otro ID", title="ERROR CREANDO ROBOT")
            return render_template('formulario_tecnico_robots.jinja')

        else: 
    
            if(tarea_exists and tarea_tipo_exists): 
                robot = Robots(id = id_robot, name=name_robot, id_Tareas = id_tarea, tipoTarea = tipo_tarea)
                db.session.add(robot)
                db.session.commit()
                return render_template('formulario_tecnico_robots.jinja')

            else:
                messagebox.showinfo(message="Campos incorrectos o incompletos, rellenelos o comprueba el ID tareas o Tipo de Tarea", title="ERROR CREANDO ROBOT")
                return render_template('formulario_tecnico_robots.jinja')


    return render_template('formulario_tecnico_robots.jinja')

@app.route("/admin/formularioUsuarios/<id_u>", methods=["GET","POST"])
def editarUsuario(id_u):
    usuarioSE =  db.session.query(Users).get(id_u)
    print(usuarioSE)
    return render_template('formulario_tecnico_usuario.jinja')



@app.route("/doctor/edit/<id>", methods=["GET","POST"])
def edit(id):
    fila_1 = db.session.query(Tabla_Medico).get(id)
    if request.method == 'POST':
        id_robot = request.form['id_robot']
        name_robot = request.form['name_robot']
        id_tarea = request.form['id_Tareas']
        tipo_tarea = request.form['tipoTarea']

        if tipo_tarea == '...':
             estado="Disponible"
        else:
             estado="Ocupado"

        fila = db.session.query(exists().where(Tabla_Medico.id_robot == id_robot)).scalar()

        if (fila):
            messagebox.showinfo(message="No se puede asignar", title="ERROR")
            return render_template('')

        else: 
            fila = Tabla_Medico(id_robot=id_robot, name_robot=name_robot, id_Tareas=id_tarea, realizando_tarea=estado,tipoTarea = tipo_tarea)
            db.session.add(fila)
            if(fila != None):
                db.session.delete(fila_1)
                db.session.commit()
            return render_template('formularioPrueba.jinja', tablas = fila_1)
    return render_template('formularioPrueba.jinja', tablas = fila_1)

    
@app.route("/admin/editarTareas/<id>", methods=["GET","POST"])
def edit_tareas(id):
    tarea_1 = db.session.query(Tareas).get(id)

    if request.method == 'POST':
        id_tarea = request.form['id']
        descripcion_tarea= request.form['descripcionTarea']
        tipo_tarea = request.form['tipo']

        tarea = Tareas(id = id_tarea, descripcionTarea = descripcion_tarea, tipo = tipo_tarea)
        db.session.add(tarea)
        if(tarea != None):
            db.session.delete(tarea_1)
            db.session.commit()
        return render_template('formulario_tecnico_tareas.jinja', tabla = tarea_1)

        
    return render_template('formulario_tecnico_tareas.jinja', tabla = tarea_1)



if __name__ == "__main__":
    app.app_context().push()
    db.drop_all()
    db.create_all()
    inserts()
    app.run(debug=True)