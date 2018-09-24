from flask import Flask, request, render_template, redirect, url_for, request
from conexiones import obtenerValores, leerString, cambioTexto
from conexiones import listaASCII, nuevaReceta, cambiarReceta
from conexiones import leerCompuesto, leerGreenTire

app = Flask(__name__)

host = "192.168.1.35"

#############################################################################################################################

@app.route('/')
def index():
	lista, datos = [], {}
	for i in range(0,299):
		var = leerString(host,i,"Medida")
		if len(var) > 1:
			compuesto = leerCompuesto(host,i)
			greenT = leerGreenTire(host,i)
			lista.append([i, var, greenT, compuesto])
			valores = obtenerValores(host,i)
			datos[i] = valores
		else:
			break
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
		lista = [variable, var, greenT, compuesto]
		valores = obtenerValores(host,variable)
		datos = {variable: valores}
	return render_template('modificar.html', i=lista, datos=datos, receta=variable)

#############################################################################################################################

@app.route('/nueva_receta')
def nueva_receta():
	return render_template('nueva_receta.html')

#############################################################################################################################

@app.route('/grabar_receta',methods=['POST'])
def grabar_receta():
	nuevaReceta(host, request)
	return redirect(url_for('index'))

#############################################################################################################################

@app.route('/cambiar_receta',methods=['POST'])
def cambiar_receta():
	cambiarReceta(host, request)
	return redirect(url_for('index'))

#############################################################################################################################

if __name__ == '__main__':
	app.run( debug=True, port=8000)