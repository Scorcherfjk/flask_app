import pyodbc 

def conexion():
    server = 'DESKTOP-QV8E63C' 
    database = 'squeegee' 
    username = 'sa' 
    password = 'Controlsi' 
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER={};DATABASE={};UID={};PWD={}'
    .format(server,database,username,password))
    cursor = cnxn.cursor()
    return cursor