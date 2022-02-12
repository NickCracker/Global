from flask import Flask             
from flask import redirect          
from flask import render_template   
from flask import request           
from flask import url_for           
from flask import session           
import pyodbc                       
import re                           
import json                         

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
"""
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint not in ['Login']:
        return redirect(url_for('Login'))
"""

#PAGINA .1 INICIO DEL SITIO : RENDERIZADO
@app.route('/')
def Login():
    return render_template('login.html')

#PAGINA .1 LOGIN AL INICIO DE SITIO : LOGICA BACKEND
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
            session['username']=request.form['usuario']
            return redirect(url_for('Buscador'))

#PAGINA .2 REGISTRO PARA USUARIOS NUEVOS : RENDERIZADO
@app.route('/registro')
def Registro():
    return render_template('registro.html')

#PAGINA .2 REGISTRO PARA USUARIOS NUEVOS : LOGICA BACKEND
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

#PAGINA .2 REGISTRO PARA USUARIOS NUEVOS : LOGICA BACKEND
@app.route('/Volver')
def Volver():
    return redirect(url_for("Login"))

#PAGINA .3 STOCK DE LOS PRODUCTOS : RENDERIZADO Y LOGICA BASICA
@app.route('/busqueda')
def Buscador():
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web ORDER BY DESCRIPCION_P;')
    data = cur.fetchall()
    for dato in data:
        dato[1]=int(dato[1])
        dato[2]=int(dato[2])
        dato[7]=int(dato[7])
    return render_template('buscador.html', valores = data)

#PAGINA .3 STOCK DE LOS PRODUCTOS CON BUSQUEDA : RENDERIZADO Y LOGICA
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
        return render_template('buscador.html', valores = resultados)

#PAGINA .4 DETALLES DE LOS PRODUCTOS : RENDERIZADO 
@app.route('/detalle/<string:id>/<string:bodega>')
def Mostrar_detalle(id,bodega):
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web where CODIGO = \''+id+'\' AND DESCRIPCION_B = \''+bodega+'\';')
    data = cur.fetchall()
    for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
            dato[7]=int(dato[7])
    return render_template('detalle.html',detalles=data[0])

#ARRANQUE DE LA APLICACION
if __name__ == '__main__' :
    app.run(port=3000,debug=True)