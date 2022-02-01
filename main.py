from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import pyodbc

"""
    En la tabla INBODEGA estan los codigos de bodega mediante CODIGO_BOD
    
"""

app = Flask(__name__)

#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_PASSWORD']=''
#app.config['MYSQL_DB']='prueba'
#mysql = MySQL(app)

s="192.168.0.97"
d="Global"
u="globalsql"
p="010101zxAS"

def conectar_base():
    conexion = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL server;SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(s,d,u,p))
    cursor = conexion.cursor()
    return cursor

@app.route('/')
def Login():
    return render_template('login.html')

@app.route('/view')
def Buscador():
    
    #MYSQL cur= mysql.connection.cursor()
    #MYSQL cur.execute('SELECT * FROM vista')

    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web')
    
    data = cur.fetchall()
    #MYSQL mysql.connection.commit()
    
    for dato in data:
        dato[1]=int(dato[1])
        dato[2]=int(dato[2])
        
    return render_template('buscador.html', valores = data)

@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        cur = conectar_base()
        
        #MYSQL cur= mysql.connection.cursor()
        #cur.execute('SELECT * FROM usuarios WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
        cur.execute('SELECT * FROM web_user_inventory WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
        
        data = cur.fetchall()
        #COMPROBAR EN BASE DE DATOS DE USUARIOS
        if data is None :
            return redirect(url_for('Login'))
        else:
            return redirect(url_for('Buscador'))

@app.route('/detalle/<string:id>')
def Mostrar_detalle(id):
    
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web where CODIGO = \''+id+'\';')
    
    #cur= mysql.connection.cursor()
    #cur.execute('SELECT * FROM vista where CODIGO = \''+id+'\';')
    
    data = cur.fetchall()
    return render_template('detalle.html',detalles=data[0])

@app.route('/view/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        codigo = request.form['codigo']
        cur = conectar_base()
        cur.execute('SELECT * FROM inve_web WHERE CODIGO=\''+codigo+'\';')
        data = cur.fetchall()
        for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
        
        return render_template('buscador.html', valores = data)
        


if __name__ == '__main__' :
    app.run(port=3000,debug=True)