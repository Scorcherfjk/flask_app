def conexion():
    import pyodbc 

    server = 'DESKTOP-QV8E63C' 
    database = 'squeegee' 
    username = 'sa' 
    password = 'Controlsi' 

    cnxn = pyodbc.connect('DRIVER=SQL Server;SERVER={0};DATABASE={1};UID={2};PWD={3}'
    .format(server,database,username,password))
    cursor = cnxn.cursor()

    cursor.execute("SELECT @@version;") 
    row = cursor.fetchone() 
    while row: 
        print(row[0]) 
        row = cursor.fetchone()

    return cursor, cnxn


def host():
    host = "192.168.1.35"
    return host