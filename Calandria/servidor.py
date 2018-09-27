from os import urandom
from io import BytesIO
from flask import Flask, request, render_template, session
from flask import redirect, url_for, request, send_file
from conexiones import obtenerValores, leerString, cambioTexto
from conexiones import nuevaReceta, cambiarReceta, eliminarReceta, insert, conexion
from conexiones import listaASCII, leerCompuesto, leerGreenTire, exportarExcel

app = Flask(__name__)
app.secret_key = urandom(24)
host = "192.168.1.35"
cursor, cnxn = conexion()

#############################################################################################################################

@app.route('/')
def login():
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

#############################################################################################################################

@app.route('/modificar/')
@app.route('/modificar/<variable>')
def modificar(variable=""):
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

#############################################################################################################################

@app.route('/nueva_receta')
def nueva_receta():
	return render_template('nueva_receta.html')

#############################################################################################################################

@app.route('/nueva_receta_simple')
def nueva_receta_simple():
	return render_template('nueva_receta_simple.html')

#############################################################################################################################

@app.route('/eliminar/')
@app.route('/eliminar/<variable>')
def eliminar(variable=""):
	if variable == "":
		return redirect(url_for('index'))
	else:
		eliminarReceta(host, variable)
	return redirect(url_for('index'))

#############################################################################################################################

@app.route('/grabar_receta',methods=['POST'])
def grabar_receta():
	insert(cursor, cnxn, request)
	nuevaReceta(host, request)
	return redirect(url_for('index'))

#############################################################################################################################

@app.route('/cambiar_receta',methods=['POST'])
def cambiar_receta():
	insert(cursor, cnxn, request)
	cambiarReceta(host, request)
	return redirect(url_for('index'))

#############################################################################################################################

@app.route('/exportar')
def exportar():
	salida = BytesIO()
	output = exportarExcel(host, salida)
	return send_file(output, attachment_filename="archivo.xlsx", as_attachment=True)

#############################################################################################################################

@app.route('/salir')
def salir():
	session.clear()
	print("sesion destruida")
	return redirect(url_for('login'))

#############################################################################################################################


if __name__ == '__main__':
	app.run( debug=True, port=8000)