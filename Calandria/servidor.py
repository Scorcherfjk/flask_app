from os import urandom
from io import BytesIO
from flask import Flask, request, render_template, session
from flask import redirect, url_for, request, send_file
from database import conexion, host
from conexiones import obtenerValores, leerString, cambioTexto
from conexiones import nuevaReceta, cambiarReceta, eliminarReceta, insert
from conexiones import listaASCII, leerCompuesto, leerGreenTire, exportarExcel, sincro_to_db, sincro_to_plc

app = Flask(__name__)
app.secret_key = urandom(24)
host = host()
try:
	cursor, cnxn = conexion()
except Exception as e:
	print(e)
	redirect(url_for('error'))


#############################################################################################################################

@app.route('/')
def login():
	if session:
		session.clear()
	return render_template('login.html')

#############################################################################################################################

@app.route('/inicio', methods=['POST'])
def entrada():
	if request.form["user"] == "admin" and request.form["passwd"] == "12345":
		session["user"] = request.form["user"]
		session["passwd"] = request.form["passwd"]
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/inicio')
def index():
	if session:
		try:
			lista, datos = [], {}
			for i in range(1,300):
				var = leerString(host,i,"Medida")
				if len(var) > 1:
					compuesto = leerCompuesto(host,i)
					greenT = leerGreenTire(host,i)
					lista.append([i, var, greenT, compuesto])
					valores = obtenerValores(host,i)
					datos[i] = valores
			return render_template('index.html', lista=lista, datos=datos)
		except TimeoutError as toe:
			print("EL PLC NO ESTA CONECTADO", toe.__class__)
			return redirect(url_for('error'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/modificar/')
@app.route('/modificar/<variable>')
def modificar(variable=""):
	if session:
		if variable == "":
			return redirect(url_for('index'))
		else:
			compuesto = leerCompuesto(host,variable)
			greenT = leerGreenTire(host,variable)
			var = leerString(host,variable,"Medida")
			valores = obtenerValores(host,variable)
			lista = [variable, var, greenT, compuesto]
			datos = {variable: valores}
		return render_template('modificar.html', i=lista, datos=datos, receta=variable)
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/nueva_receta')
def nueva_receta():
	if session:
		return render_template('nueva_receta.html')
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/nueva_receta_simple')
def nueva_receta_simple():
	if session:
		return render_template('nueva_receta_simple.html')
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/eliminar/')
@app.route('/eliminar/<variable>')
def eliminar(variable=""):
	if session:
		if variable == "":
			return redirect(url_for('index'))
		else:
			eliminarReceta(host, variable)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/grabar_receta',methods=['POST'])
def grabar_receta():
	if session:
		insert(cursor, cnxn, request)
		nuevaReceta(host, request)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/cambiar_receta',methods=['POST'])
def cambiar_receta():
	if session:
		insert(cursor, cnxn, request)
		cambiarReceta(host, request)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/db_to_plc')
def db_to_plc():
	if session:
		sincro_to_plc(host, cursor, cnxn)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/plc_to_db')
def plc_to_db():
	if session:
		sincro_to_db(host, cursor, cnxn)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/exportar')
def exportar():
	if session:
		salida = BytesIO()
		output = exportarExcel(host, salida)
		archivo = "nombre_archivo"
		return send_file(output, attachment_filename=archivo+".xlsx", as_attachment=True)
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/error')
def error():
	if session:
		session.clear()
	return render_template('error.html')

#############################################################################################################################

@app.route('/salir')
def salir():
	session.clear()
	print("sesion destruida")
	return redirect(url_for('login'))

#############################################################################################################################


if __name__ == '__main__':
	app.run( debug=True, port=8000)