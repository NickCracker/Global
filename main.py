from flask import Flask,redirect,render_template,request,url_for,session
import pyodbc
import re
import json

#Instanciacion del modulo Flask
app = Flask(__name__)
route = '.conexion.json'
acceso = False

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
        cur.execute('INSERT INTO web_user_inventory VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\');'.format(nombre,apellido,usuario,correo,contraseña))
        cur.connection.commit()
        cur.connection.close()
        return redirect(url_for("Login"))
    else:
        return redirect(url_for("Registro"))

#Redireccion a la pagina de busqueda y consulta de datos
@app.route('/busqueda')
def Buscador():
    if session['user'] != "":
        cur = conectar_base()
        cur.execute('SELECT * FROM inve_web ORDER BY DESCRI_MAT')
        data = cur.fetchall()
        for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
        return render_template('buscador.html', valores = data)
    else:
        return redirect(url_for("Login"))

#Logica del login, redirecciona al login si hay error y da acceso al buscador si se registra bien
@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cur = conectar_base()
        cur.execute('SELECT * FROM web_user_inventory WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
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
    cur.execute('SELECT * FROM detalles_inve where CODIGO = \''+id+'\';')
    data = cur.fetchall()
    return render_template('detalle.html',detalles=data[0])

#Resultados de la busqueda con filtro
@app.route('/busqueda/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST' and acceso:
        entrada = request.form['entrada']
        cur = conectar_base()
        cur.execute('SELECT * FROM inve_web;')
        data = cur.fetchall()
        patron = r"^{0}".format(entrada)
        resultados = []
        for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
            if re.match(patron,dato[3]) :
                resultados.append(dato) 
        return render_template('buscador.html', valores = resultados)
        
#Inicio del programa
if __name__ == '__main__' :
    app.run(port=3000,debug=True)