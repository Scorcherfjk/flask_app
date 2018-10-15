from os import urandom
from io import BytesIO
from datetime import datetime
from flask import Flask, request, render_template, session
from flask import redirect, url_for, request, send_file
from database import conexion, host
from conexiones import obtenerValores, leerString, cambioTexto, inicio, usuario
from conexiones import nuevaReceta, cambiarReceta, eliminarReceta, nuevaReceta_db
from conexiones import listaASCII, leerCompuesto, leerGreenTire, exportarExcel, sincronia
from conexiones import sincro_to_db, sincro_to_plc, insert, leer_db, cambiarTolerancia
from conexiones import cambiarReceta_db, leer_elemento, tolerancia, eliminarReceta_db, cargado

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
	usuarios = usuario(cursor)
	for i in usuarios:
		if request.form["user"] == usuarios[i][0] and request.form["passwd"] == usuarios[i][1]:
			session["user"] = request.form["user"]
			session["passwd"] = request.form["passwd"]
			session["rol"] = usuarios[i][2]
			return redirect(url_for('index'))
	return redirect(url_for('login'))

#############################################################################################################################

@app.route('/database')
def index():
	if session:
		lista, datos = [], {}
		sincro = sincronia(cursor)
		tol = tolerancia(cursor)
		values = inicio(cursor)
		for i in values:
			compuesto = i["Compuesto"]
			greenT = i["GreenTire"]
			lista.append([i["i"], i["medida"], greenT, compuesto])
			valores = [ i["PresionRodillo"], i["VelocidadMax"], i["diferencia_yellow"], i["diferencia_red"], i["diferencia_blue"], i["dim_a_Comp_A"], i["dim_a_Comp_B"], i["dim_b_Comp_A"], i["dim_b_Comp_B"], i["AnchoSqueegee_Comp_A"], i["AnchoSqueegee_Comp_B"], i["AnchoPliego_Comp_A"], i["AnchoPliego_Comp_B"], i["CalibreCaliente_Comp_A"], i["CalibreCaliente_Comp_B"], i["PliegoMesaAlta"], i["fecha_modificacion"] ]
			datos[i["i"]] = valores
		return render_template('database.html' 
								,lista=lista
								,datos=datos
								,rol=session["rol"]
								,tol=tol
								,user=session["user"]
								,sincro=sincro)
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/plc_actual')
def plc_actual():
	if session:
		try:
			lista, datos = [], {}
			tol = tolerancia(cursor)
			for i in range(1,300):
				var = leerString(host,i,"Medida")
				if len(var) > 1:
					compuesto = leerCompuesto(host,i)
					greenT = leerGreenTire(host,i)
					lista.append([i, var, greenT, compuesto])
					valores = obtenerValores(host,i)
					datos[i] = valores
			return render_template('plc.html', lista=lista, datos=datos, rol=session["rol"], user=session["user"], tol=tol)
		except TimeoutError as toe:
			print("EL PLC NO ESTA CONECTADO", toe.__class__)
			return redirect(url_for('error'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/historico')
def historico():
	if session:
		lista, datos = [], {}
		values = leer_db(cursor)
		for i in values:
			compuesto = i["Compuesto"]
			greenT = i["GreenTire"]
			lista.append([i["i"], i["medida"], greenT, compuesto])
			valores = [ i["PresionRodillo"], i["VelocidadMax"], i["diferencia_yellow"], i["diferencia_red"], i["diferencia_blue"], i["dim_a_Comp_A"], i["dim_a_Comp_B"], i["dim_b_Comp_A"], i["dim_b_Comp_B"], i["AnchoSqueegee_Comp_A"], i["AnchoSqueegee_Comp_B"], i["AnchoPliego_Comp_A"], i["AnchoPliego_Comp_B"], i["CalibreCaliente_Comp_A"], i["CalibreCaliente_Comp_B"], i["PliegoMesaAlta"], i["fecha_modificacion"], i["usuario"] ]
			datos[i["i"]] = valores
		return render_template('historico.html', lista=lista, datos=datos, rol=session["rol"], user=session["user"])
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
			tol = tolerancia(cursor)
			i = leer_elemento(cursor, variable)
			compuesto = i["Compuesto"]
			greenT = i["GreenTire"]	
			lista = [variable, i["medida"], greenT, compuesto]
			valores = [ i["PresionRodillo"], i["VelocidadMax"],0,0,0, i["dim_a_Comp_A"], i["dim_a_Comp_B"], i["dim_b_Comp_A"], i["dim_b_Comp_B"], i["AnchoSqueegee_Comp_A"], i["AnchoSqueegee_Comp_B"], i["AnchoPliego_Comp_A"], i["AnchoPliego_Comp_B"], i["CalibreCaliente_Comp_A"], i["CalibreCaliente_Comp_B"], i["PliegoMesaAlta"] ]
			datos = {variable: valores}
		return render_template('modificar.html', i=lista, datos=datos, receta=variable, rol=session["rol"], user=session["user"], tol=tol)
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/nueva_receta')
def nueva_receta():
	if session:
		tol = tolerancia(cursor)
		return render_template('nueva_receta.html', rol=session["rol"], user=session["user"], tol=tol)
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/nueva_receta_simple')
def nueva_receta_simple():
	if session:
		tol = tolerancia(cursor)
		return render_template('nueva_receta_simple.html', rol=session["rol"], user=session["user"], tol=tol)
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
			eliminarReceta_db(cursor, cnxn, variable)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/grabar_receta',methods=['POST'])
def grabar_receta():
	if session:
		insert(cursor, cnxn, request, session)
		nuevaReceta_db(host, cursor, cnxn, request)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/cambiar_receta',methods=['POST'])
def cambiar_receta():
	if session:
		insert(cursor, cnxn, request, session)
		cambiarReceta_db(host, cursor, cnxn, request)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/db_to_plc')
def db_to_plc():
	if session:
		sincro_to_plc(host, cursor, cnxn)
		cargado(cursor, cnxn, session)
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
		dt = datetime.now()
		salida = BytesIO()
		output = exportarExcel(cnxn, salida)
		archivo = "Recetas_Calandria_4R_{}/{}/{}_{}:{}:{}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
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

@app.route('/tolerancia')
def control_tolerancia():
	if session:
		tol = tolerancia(cursor)
		return render_template('tolerancia.html', rol=session["rol"], user=session["user"], tol=tol)
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/cambiar_tolerancia',methods=['POST'])
def cambiar_tolerancia():
	if session:
		cambiarTolerancia(cursor, cnxn, request)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('login'))

#############################################################################################################################

@app.route('/salir')
def salir():
	session.clear()
	print("sesion destruida")
	return redirect(url_for('login'))

#############################################################################################################################


if __name__ == '__main__':
	app.run( host="192.168.1.41",port=5010)