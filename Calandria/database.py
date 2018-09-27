import pyodbc 

def dbcursor():
    server = 'DESKTOP-QV8E63C' 
    database = 'squeegee' 
    username = 'sa' 
    password = 'Controlsi' 
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER={0};DATABASE={1};UID={2};PWD={3}'
    .format(server,database,username,password))
    cursor = cnxn.cursor()
    return cursor, cnxn