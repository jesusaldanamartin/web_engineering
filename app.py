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
from datetime import datetime, timedelta


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
    tipo_tarea = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task id={self.id} tipo={self.tipo_tarea} date={self.date}>"

class Admin(db.Model):
    __tablename__ = 'Administrators'
    admin = db.Column(db.String(100), db.ForeignKey(Users.id), primary_key= True)

    def __repr__(self):
        return '<admin %r>' % self.admin

class Incidencias(db.Model):
    __tablename__ = 'Incidencias'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    asunto = db.Column(db.String(100), nullable=False)
    informe = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Incidencia id={self.id} Asunto ={self.informe} Informe={self.informe}>"

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
    date = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<Robot id={self.id} name={self.name} id_Tarea={self.id_Tareas} date={self.date}>"

class Tabla_Medico(db.Model):
    __tablename__ = 'Tabla medico'
    id_robot = db.Column(db.String(150), nullable=False, primary_key= True)
    name_robot = db.Column(db.String(150), db.ForeignKey(Robots.name))
    id_Tareas = db.Column(db.String(100), db.ForeignKey(Tareas.id))
    estado = db.Column(db.String(150),nullable=False )
    tipoTarea = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(150), nullable=True)
    
    def __iter__(self):
        return self

    def __repr__(self):
        return f"<TablaMedica id={self.id_robot} name={self.name_robot} id_Tarea={self.id_Tareas} tipoTarea={self.tipoTarea} realizandoTarea={self.realizando_tarea} date={self.date}>"


#class AsignarTareasRobots(db.Model):
#    __tablename__ = "Tabla asignar tareas robots"
#    tipo_tarea = db.Column(db.String(120), db.ForeignKey(Tareas.tipo_tarea)) #* Limpieza, Transporte y Telemedicina
#    tipo_tarea_asignada = db.Column(db.String(120), nullable= False) #* impieza de habitacion, Desinfeccion; Transporte de comida y Transporte de farmacos; Telemedicina
#    id_Tareas = db.Column(db.String(100), db.ForeignKey(Tareas.id)) #* 0,1,2,3
#    nombre_robot = db.Column(db.String(150), db.ForeignKey(Robots.name))
#    id_robot = db.Column(db.String(150), db.ForeignKey(Robots.id))
#    estado = db.Column(db.String(100), db.ForeignKey(Tabla_Medico.estado)) #* Ocupado o Disponible
#  
#    def __repr__(self):
#        return f"<TablaAsignarTareas tipo_tarea={self.tipo_tarea} tarea_asignada={self.tipo_tarea_asignada} id_Tarea={self.id_Tareas} nombreRobot={self.nombre_robot} idRobot={self.id_robot} estado={self.estado}>"


def inserts():
    admin = Users(id=0, name="admin", email="email_admin@example.com", password="admin", status="admin")

    usr1 = Users(id="10", name="person1", email="email_medico1@example.com", password="1", status="medico")
    usr2 = Users(id="20", name="person2", email="email_medico2@example.com", password="2", status="medico")
    usr3 = Users(id="30", name="person3", email="email_medico3@example.com", password="3", status="medico")
    usr4 = Users(id="40", name="person4", email="email_medico4@example.com", password="4", status="medico")
    usr5 = Users(id="50", name="person5", email="email_medico5@example.com", password="5", status="medico")

    tarea100 = Tareas(id = "100", tipo_tarea = "Limpieza")
    tarea200 = Tareas(id = "200", tipo_tarea = "Transporte")
    tarea300 = Tareas(id = "300", tipo_tarea = "Desinfeccion")
    tarea400 = Tareas(id = "400", tipo_tarea = "Telemedicina")
    tarea500 = Tareas(id = "500", tipo_tarea = "Limpieza y Desinfeccion")

    robotA = Robots(id = "0", name = "Robot-A", id_Tareas = "100")
    robotB = Robots(id = "1", name = "Robot-B", id_Tareas = "200")
    robotC = Robots(id = "2", name = "Robot-C", id_Tareas = "100")
    robotD = Robots(id = "3", name = "Robot-D", id_Tareas = "400")
    robotE = Robots(id = "4", name = "Robot-E", id_Tareas = "200")
    robotF = Robots(id = "5", name = "Robot-F", id_Tareas = "200")
    robotG = Robots(id = "6", name = "Robot-G", id_Tareas = "300")
    robotH = Robots(id = "7", name = "Robot-H", id_Tareas = "300")
    robotI = Robots(id = "8", name = "Robot-I", id_Tareas = "500")
    robotJ = Robots(id = "9", name = "Robot-J", id_Tareas = "400")
 

    accion1 = Tabla_Medico(id_robot="0", name_robot="Robot1", id_Tareas="100", estado="Ocupado",tipoTarea="Limpieza pasillo" )
    accion2 = Tabla_Medico(id_robot="1", name_robot="Robot2", id_Tareas="200", estado="Disponible",tipoTarea="..." )

    #asg_tareas = AsignarTareasRobots(tipo_tarea="Limpieza",tipo_tarea_asignada="...",id_Tareas="100",nombre_robot="",id_robot=,estado=)

    db.session.add(admin)
    db.session.commit()
    db.session.add(usr1)
    db.session.commit()
    db.session.add(usr2)
    db.session.commit()
    db.session.add(usr3)
    db.session.commit()
    db.session.add(usr4)
    db.session.commit()
    db.session.add(usr5)
    db.session.commit()

    db.session.add(tarea100)
    db.session.commit()
    db.session.add(tarea200)
    db.session.commit()
    db.session.add(tarea300)
    db.session.commit()
    db.session.add(tarea400)
    db.session.commit()
    db.session.add(tarea500)
    db.session.commit()

    db.session.add(robotA)
    db.session.commit()
    db.session.add(robotB)
    db.session.commit()
    db.session.add(robotC)
    db.session.commit()
    db.session.add(robotD)
    db.session.commit()
    db.session.add(robotE)
    db.session.commit()
    db.session.add(robotF)
    db.session.commit()
    db.session.add(robotG)
    db.session.commit()
    db.session.add(robotH)
    db.session.commit()
    db.session.add(robotI)
    db.session.commit()
    db.session.add(robotJ)
    db.session.commit()

    db.session.add(accion1)
    db.session.commit()
    db.session.add(accion2)
    db.session.commit()
    # db.session.add(accion3)
    # db.session.commit()


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
    incidencias_db = db.session.query(Incidencias).all()

    #for user in usuarios_db: print(user.name)
    #for task in tareas_db: print(task.name)
    #for robot in robots_db: print(robot.name)

    return render_template('template_tecnico.jinja', usuarios = usuarios_db, tareas = tareas_db, robots = robots_db, incidencias = incidencias_db)

@app.route("/doctor", methods=["GET", "POST"])
def doctor():
    robots_db = db.session.query(Robots).all()
    tareas_db = db.session.query(Tareas).all()
    accion_db = db.session.query(Tabla_Medico).all()
    # ini_time_for_now = datetime.now()
    # for elems in accion_db:
    #     new_final_time = ini_time_for_now - \
    #              accion_db.testimado
    

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

@app.route("/doctor/<id>")
def robot(id):
    robot = db.session.query(Robots).get(id)
    acciones = db.session.query(Tabla_Medico).filter_by(name_robot=robot.name)

    return render_template('template_robot.jinja', robot= robot, acciones = acciones)

@app.route("/admin/formularioTareas", methods=["GET","POST"])
def tarea():
    tareaNula = Tareas()
    if request.method == 'POST':
        id_tarea = request.form['id']
        tipo_tarea = request.form['tipo_tarea']
        tarea_exists = db.session.query(exists().where(Tareas.id == id_tarea)).scalar()

        if (tarea_exists):
            flash('ERROR: La tarea ya existe o faltan campos por rellenar')
            return render_template('formulario_tecnico_tareas.jinja')

        else: 
            tarea = Tareas(id = id_tarea, tipo_tarea = tipo_tarea)
            db.session.add(tarea)
            db.session.commit()
            flash('¡Tarea creada con éxito!')
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
            flash('ERROR: El usuario ya existe, prueba otro ID')
            return render_template('formulario_tecnico_usuario.jinja')

        else:
            usuario = Users(id = id_usuario, name = name_usuario, email = email_usuario, password = password_usuario, status = status_usuario)
            db.session.add(usuario)
            db.session.commit()
            
            flash('¡Usuario creado con éxito!')
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

        if (robot_exists):
            flash('ERROR: Este robot ya existe, prueba otro ID')
            return render_template('formulario_tecnico_robots.jinja')

        else: 
    
            if(tarea_exists): 
                robot = Robots(id = id_robot, name=name_robot, id_Tareas = id_tarea)
                db.session.add(robot)
                db.session.commit()
                
                flash('¡Robot creado con éxito!')
                return render_template('formulario_tecnico_robots.jinja')

            else:
                flash("ERROR: Campos incompletos o incorrectos, comprueba el ID tareas o Tipo de Tarea")
                return render_template('formulario_tecnico_robots.jinja')


    return render_template('formulario_tecnico_robots.jinja')

@app.route("/admin/formularioUsuarios/<id_u>", methods=["GET","POST"])
def editarUsuario(id_u):
    usuarioSE =  db.session.query(Users).get(id_u)
    print(usuarioSE)
    return render_template('formulario_tecnico_usuario.jinja')



@app.route("/doctor/asignarTareas/<id>", methods=["GET","POST"])
def edit(id):
    fila_1 = db.session.query(Tabla_Medico).get(id)
    tarea = db.session.query(Tareas).all()
    print(tarea)
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
            fila = Tabla_Medico(id_robot=id_robot, name_robot=name_robot, id_Tareas=id_tarea, estado=estado,tipoTarea = tipo_tarea)
            db.session.add(fila)
            if(fila != None):
                db.session.delete(fila_1)
                db.session.commit()
            return render_template('formulario_tabla_medico.jinja', tablas = fila_1 , tarea = tarea)
    return render_template('formulario_tabla_medico.jinja', tablas = fila_1, tarea=tarea)

@app.route("/doctor/formularioIncidencia", methods=["GET","POST"])
def incidencia():

    if request.method == 'POST':
        # id_incidencia = request.form['id']
        asunto = request.form['asunto']
        informe = request.form['informe']
        incidencia = Incidencias(asunto = asunto, informe = informe)
        db.session.add(incidencia)
        db.session.commit()
            
    
    return render_template('formulario_incidencia_medico.jinja')

    
@app.route("/admin/formularioTareas/<id>", methods=["GET","POST"])
def edit_tareas(id):
    tarea_1 = db.session.query(Tareas).get(id)
 
    if request.method == 'POST':
        id_tarea = request.form['id']
        #descripcion_tarea= request.form['descripcionTarea']
        tipo_tarea = request.form['tipo_tarea']

        tarea = Tareas(id = id_tarea, tipo_tarea=tipo_tarea)
        db.session.add(tarea)
        if(tarea != None):
            db.session.delete(tarea_1)
            db.session.commit()
        return render_template('formulario_tecnico_tareas.jinja', tabla = tarea)

    return render_template('formulario_tecnico_tareas.jinja', tabla = tarea_1)



if __name__ == "__main__":
    app.app_context().push()
    db.drop_all()
    db.create_all()
    inserts()
    app.run(debug=True)