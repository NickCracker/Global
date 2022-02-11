from flask import Flask             #Microframework para trabajar en la web con python
from flask import redirect          #Para poder redireccionar de una pagina a otra
from flask import render_template   #Para poder renderizar las paginas
from flask import request           #Para obtener valores de los formularios
from flask import url_for           #Para obtener la url de algun elemento(funciones)
from flask import make_response     #Para realizar respuestas al servidor
from flask import session           #Para crear y eliminar sesiones
import pyodbc                       #Para conectarse a la base de datos de SQL Server
import re                           #Para verificar entradas validas
import json                         #Para utilizar archivos JSON

#Instanciacion del modulo Flask
app = Flask(__name__)
route = '.conexion.json'
def carga(ruta):
    with open(ruta) as contenido:
        datos = json.load(contenido)
        return datos    
datos = carga(route)
app.secret_key = datos.get('clave','')

#Datos para la conexion con SQL Server
servidor = datos.get('server','')
base = datos.get('database','')
usuario = datos.get('user','')
contraseña = datos.get('password','')

#Esta funcion permite conectar a la base de datos SQL Server y retorna un curso
def conectar_base():
    conexion = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL server;SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(servidor,base,usuario,contraseña))
    cursor = conexion.cursor()
    return cursor

#<-------------------------------------------PAGINA WEB-------------------------------------------------->

#Redireccion al login 
@app.route('/')
def Login():
    return render_template('login.html')

@app.route('/registro')
def Registro():
    return render_template('registro.html')

@app.route('/Registrar', methods=['POST'])
def Registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        cur = conectar_base()
        cur.execute('INSERT INTO users_web VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\');'.format(nombre,apellido,usuario,correo,contraseña))
        cur.connection.commit()
        cur.connection.close()
        return redirect(url_for("Login"))
    else:
        return redirect(url_for("Registro"))

@app.route('/Volver')
def Volver():
    return redirect(url_for("Login"))

#Redireccion a la pagina de busqueda y consulta de datos
@app.route('/busqueda')
def Buscador():
    if session['user'] != "":
        cur = conectar_base()
        cur.execute('SELECT * FROM inve_web ORDER BY DESCRIPCION_P;')
        data = cur.fetchall()
        for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
            dato[7]=int(dato[7])
        return render_template('buscador.html', valores = data)
    else:
        return redirect(url_for("Login"))

#Resultados de la busqueda con filtro
@app.route('/busqueda/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        entrada = request.form['entrada']
        cur = conectar_base()
        cur.execute('SELECT * FROM inve_web;')
        data = cur.fetchall()
        patron = r"^{0}".format(entrada)
        resultados = []
        for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
            if re.match(patron.upper(),dato[3]) :
                resultados.append(dato) 
            dato[7]=int(dato[7])
        return render_template('buscador.html', valores = resultados)

#Logica del login, redirecciona al login si hay error y da acceso al buscador si se registra bien
@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cur = conectar_base()
        cur.execute('SELECT * FROM users_web WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
        data = cur.fetchall()
        if len(data) == 0 :
            return redirect(url_for('Login'))
        else:
            session['user'] = usuario
            return redirect(url_for('Buscador'))

#Redirecciona a la pagina de detalles 
@app.route('/detalle/<string:id>')
def Mostrar_detalle(id):
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web where CODIGO = \''+id+'\';')
    data = cur.fetchall()
    return render_template('detalle.html',detalles=data[0])

#Inicio del programa
if __name__ == '__main__' :
    app.run(port=3000,debug=True)