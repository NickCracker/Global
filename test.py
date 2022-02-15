#Importaciones
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session
import json
import pymysql

#Funcion de carga de datos JSON
route = '.conexion.json'
def carga(ruta):
    with open(ruta) as contenido:
        datos = json.load(contenido)
        return datos    
datos = carga(route)

#Datos para la conexion con SQL Server
servidor = datos.get('server','')
base = datos.get('database','')
usuario = datos.get('user','')
contraseña = datos.get('password','')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=datos.get('correo','')
app.config['MAIL_PASSWORD']=datos.get('cc','')

db = SQLAlchemy(app)
mail = Mail()

class Producto(db.Model):
    __tablename__ = 'new_inve_web'
    codigo=db.Column(String(50),primary_key=True)
    descripcion=db.Column(String(150))
    stock=db.Column(Integer())
    reserva=db.Column(Integer())
    clase=db.Column(String(50))
    subclase=db.Column(String(50))
    laboratorio=db.Column(String(50))
    precio=db.Column(Integer())
    lote=db.Column(String(50))
    bodega=db.Column(String(50))
    ubicacion=db.Column(String(50))

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    correo=db.Column(String(50),primary_key=True)
    nombre=db.Column(String(50))
    usuario=db.Column(String(50))
    contraseña=db.Column(String(50))
    
db.init_app(app)
mail.init_app(app)
app.secret_key=datos.get("clave","")

#PAGINA 1: LOGIN / RENDERIZA LA PAGINA DEL LOGIN Y ENVIA LOS DATOS
@app.route('/')
def Login():
    if 'username' in session:
        return redirect(url_for('Buscador'))
    else:
        return render_template('login.html')

#PAGINA 1: LOGIN / BUSCA LOS DATOS EN LA BASE DE DATOS Y REDIRECCIONA EN FUNCION DEL RESULTADO DE LA QUERY
@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        coincidencias = Usuario.query.filter(Usuario.usuario==usuario and Usuario.contraseña==contraseña)
        for coincidencia in coincidencias:
            if coincidencia.nombre != '':
                session['username']=usuario
                return redirect(url_for('Buscador'))
        return redirect(url_for('Login'))

#PAGINA 2: REGISTRO / RENDERIZA LA PAGINA DEL REGISTRO Y ENVIA LOS DATOS
@app.route('/registro')
def Registro():
    return render_template('registro.html')

#PAGINA 2: REGISTRO / EVALUA SI LOS DATOS INGRESADOS SON VALIDOS Y REDIRECCIONA EN FUNCION DE ELLOS
@app.route('/Registrar', methods=['POST'])
def Registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        if not '' in [nombre,usuario,correo,contraseña] :
            usuario_nuevo = Usuario(nombre=nombre,usuario=usuario,correo=correo,contraseña=contraseña)
            db.session.add(usuario_nuevo)
            db.session.commit()
            msg = Message("Se ha registrado con exito",sender=app.config['MAIL_USERNAME'],recipients=[correo])
            msg.html = render_template('email.html',usuario = usuario)
            mail.send(msg)
        return redirect(url_for('Login'))

#PAGINA 2: REGISTRO / RETORNA AL LOGIN EN CASO DE QUE EL USUARIO ASI LO QUIERA
@app.route('/Volver')
def Volver():
    return redirect(url_for("Login"))

#PAGINA 3: BUSCADOR / REALIZA LA CONSULTA A LA BASE DE DATOS Y RENDERIZA LA TABLA
@app.route('/busqueda')
@app.route('/busqueda/<int:pagina>')
def Buscador(pagina=1):
    if 'username' in session:
        print(session['username'])
        per_page = 25
        productos = Producto.query.add_columns(Producto.codigo,Producto.descripcion,Producto.stock,Producto.reserva,Producto.lote).order_by(Producto.descripcion).paginate(pagina,per_page,False)
        return render_template('buscador.html',productos=productos,pagina=pagina)
    else:
        return redirect(url_for("Login"))

#PAGINA 3: BUSCADOR / TOMA LA ENTRADA DEL USUARIO PARA BUSCAR Y MOSTRAR COINCIDENCIAS
@app.route('/busqueda/buscar', methods=['POST'])
def Buscar():
    if request.method == 'POST':
        entrada = request.form['entrada']
        productos = Producto.query.add_columns(Producto.codigo,Producto.descripcion,Producto.stock,Producto.reserva,Producto.lote).filter(Producto.descripcion.like(''+entrada+'%')).order_by(Producto.descripcion).paginate(1,335,False)
        return render_template('buscador.html',productos=productos)

#PAGINA 4: DETALLE / MUESTRA EL RESTO DE DATOS DEL PRODUCTO SELECCIONADO EN EL BUSCADOR
#DEBO CAMBIAR LA PRIMARY KEY POR EL LOTE, EN CASO DE NO TENER LOTE BUSCAR POR CODIGO
@app.route('/detalle/<string:codigo>/<string:lote>')
def Mostrar_detalle(codigo,lote):
    if 'username' in session:
        producto = Producto.query.filter(Producto.lote==lote).first()
        return render_template('detalle.html',producto=producto)
    else:
        return redirect(url_for('Login'))

if __name__ == '__main__':
    app.run(debug=True,port=5000)
