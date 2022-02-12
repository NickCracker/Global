from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import re

#Instanciacion del modulo Flask
app = Flask(__name__)

#Datos para la conexion con MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'
mysql = MySQL(app)
app.secret_key='mysecretkey'

#<-------------------------------------------PAGINA WEB-------------------------------------------------->

#Redireccion al login 
@app.route('/')
def Login():
    return render_template('login.html')

#Logica del login, redirecciona al login si hay error y da acceso al buscador si se registra bien
@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
        data = cur.fetchall()
        if len(data)!=0:
            return redirect(url_for("Buscador"))
        else:
            return redirect(url_for("Login"))
    else:
        return False

@app.route('/busqueda')
def Buscador():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM new_inve_web ;')
    data = cur.fetchall()
    return render_template('buscador.html', valores = data)
    
#Redirecciona a la pagina de detalles 
@app.route('/detalle/<string:id>')
def Mostrar_detalle(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM new_inve_web where CODIGO = \''+id+'\';')
    data = cur.fetchall()
    return render_template('detalle.html',detalles=data[0])

#Resultados de la busqueda con filtro
@app.route('/busqueda/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        entrada = request.form['entrada']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM new_inve_web where DESCRIPCION LIKE \'{0}%\';'.format(entrada))
        data = cur.fetchall()
        return render_template('buscador.html', valores = data)
        
#Inicio del programa
if __name__ == '__main__' :
    app.run(port=3000,debug=True)