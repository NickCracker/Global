from flask import Flask, redirect, render_template, request, url_for
import pyodbc
import re

# Variables de entorno.
import os
from dotenv import load_dotenv
config = load_dotenv(".env")

#Instanciacion del modulo Flask
app = Flask(__name__)

#Datos para la conexion con SQL Server
servidor = os.environ.get('servidor')
base = os.environ.get('base')
usuario = os.environ.get('usuario')
contraseña = os.environ.get('contraseña')

#Esta funcion permite conectar a la base de datos SQL Server y retorna un curso
def conectar_base():
    conexion = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL server;SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(servidor,base,usuario,contraseña))
    cursor = conexion.cursor()
    return cursor

#Redireccion al login 
@app.route('/')
def Login():
    return render_template('login.html')

#Redireccion a la pagina de busqueda y consulta de datos
@app.route('/busqueda')
def Buscador():
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web ORDER BY DESCRI_MAT')
    data = cur.fetchall()
    for dato in data:
        dato[1]=int(dato[1])
        dato[2]=int(dato[2])
    return render_template('buscador.html', valores = data)

#Logica del login, redirecciona al login si hay error y da acceso al buscador si se registra bien
@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cur = conectar_base()
        cur.execute('SELECT * FROM web_user_inventory WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
        data = cur.fetchall()
        if data is None :
            return redirect(url_for('Login'))
        else:
            return redirect(url_for('Buscador'))

#Redirecciona a la pagina de detalles 
@app.route('/detalle/<string:id>')
def Mostrar_detalle(id):
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web where CODIGO = \''+id+'\';')
    data = cur.fetchall()
    return render_template('detalle.html',detalles=data[0])

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
            if re.match(patron,dato[3]) :
                resultados.append(dato)
            
        return render_template('buscador.html', valores = resultados)
        
#Inicio del programa
if __name__ == '__main__' :
    app.run(port=3000,debug=True)