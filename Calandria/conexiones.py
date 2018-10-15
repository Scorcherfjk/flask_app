def listaASCII(texto):
    a = [ord(i) for i in texto]
    return a

#############################################################################################################################

def listaSTRING(ASCII):
    a = ''.join(chr(i) for i in ASCII)
    return a

#############################################################################################################################

def limpiatexto(string):
    lista = string.split(",")
    resultado = []
    for i in lista:
        resultado.append(listaASCII(i.strip()))
    return resultado[:5]

#############################################################################################################################

def limpiatextoC(lista):
    resultado = []
    for i in lista:
        resultado.append(listaASCII(i.strip()))
    return resultado[:5]

#############################################################################################################################

def matriz(host):
    lista = []
    for i in range(1,300):
        var = leerString(host,i,"Medida")
        if len(var) > 1:
            PliegoMesaAlta = leerString(host,i,"PliegoMesaAlta")
            compuesto = leerCompuesto(host,i)
            greenT = leerGreenTire(host,i)
            valores = obtenerValores(host,i)

            lista.append([i, var, PliegoMesaAlta, greenT, valores[0], valores[1], 
            compuesto[0], valores[13], valores[9], valores[11], valores[5], valores[7],
            compuesto[1], valores[14], valores[10], valores[12], valores[6], valores[8],
            valores[2], valores[3], valores[4]])

    return lista

#############################################################################################################################

def DINT(host, tags):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            if value == True or value == False:
                yield value
            else:
                yield value[0]

#############################################################################################################################

def leerString(host,indice,etiqueta):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    
    tags = ["RecetasPL[{}].{}.LEN".format(indice,etiqueta)]
    
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2):
            val = str(value[0])
            valor = ["RecetasPL[{}].{}.Data[0-{}]".format(indice,etiqueta,val)]
            with connector( host=host ) as conn:
                for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( valor ), depth=2):
                    final = ''.join(chr(i) for i in value).strip("\x00")
                    return final

#############################################################################################################################

def obtenerValores(host, i):
    lista = []
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    
    tags=[
            "RecetasPL[{}].PresionRodillo".format(i),
            "RecetasPL[{}].VelocidadMax".format(i),
            "RecetasPL[{}].Dif_LinerToegard_Yellow".format(i),
            "RecetasPL[{}].Dif_LinerToegard_Red".format(i),
            "RecetasPL[{}].Dif_LinerToegard_Blue".format(i),
            "RecetasPL[{}].DIM_A_Comp_A".format(i),
            "RecetasPL[{}].DIM_A_Comp_B".format(i),
            "RecetasPL[{}].DIM_B_Comp_A".format(i),
            "RecetasPL[{}].DIM_B_Comp_B".format(i),
            "RecetasPL[{}].AnchoSqueegee_Comp_A".format(i),
            "RecetasPL[{}].AnchoSqueegee_Comp_B".format(i),
            "RecetasPL[{}].AnchoPliego_Comp_A".format(i),
            "RecetasPL[{}].AnchoPliego_Comp_B".format(i),
            "RecetasPL[{}].CalibreCaliente_Comp_A".format(i),
            "RecetasPL[{}].CalibreCaliente_Comp_B".format(i)
         ]

    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            lista.append(value[0])

    a = leerString(host,i,"PliegoMesaAlta")
    lista.append(a)
    lista[13] = float("{0:.2f}".format(lista[13]))
    lista[14] = float("{0:.2f}".format(lista[14]))
    lista[2] = lista[8] - lista[7]
    lista[3] = lista[2] * 2 + lista[10]
    lista[4] = (lista[12] - lista[3]) / 2
    return lista

#############################################################################################################################

def cambioTexto(host,elemento,columna,ASCII):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    
    tags = []
    
    for index, value in enumerate(ASCII):
        tags.append("RecetasPL[{}].{}.DATA[{}]=(SINT){}".format(elemento,columna,index,value))

    resultado = []
    
    tags.append("RecetasPL[{}].{}.LEN=(DINT){}".format(elemento,columna,len(tags)))

    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            resultado.append(value)
        
    return resultado, tags

#############################################################################################################################
    
def nuevaReceta(host, request):
    for l in range(1,300):
        var = leerString(host,l,"Medida")
        if len(var) > 1:
            pass
        else:
            i = l
            break
    lista = []
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client

    cambioTexto(host,i,"Medida",listaASCII(request.form["PLIEGODEGOMA"]))
    cambioTexto(host,i,"PliegoMesaAlta",listaASCII(request.form["PLIEGODEMESAALTA"]))
    escribirGreenTire(host,i,request.form["GREENTIRE"])
    escribirCompuesto(host,i,[request.form["COMPUESTOA"],request.form["COMPUESTOB"]])

    tags=[
           "RecetasPL[{}].PresionRodillo=(DINT){}".format(i,int(request.form["PRESIÓNDERODILLO"])),
           "RecetasPL[{}].VelocidadMax=(DINT){}".format(i,int(request.form["VELOCIDADMAXIMA"])),
           "RecetasPL[{}].DIM_A_Comp_A=(DINT){}".format(i,int(request.form["DIMAA"])),
           "RecetasPL[{}].DIM_A_Comp_B=(DINT){}".format(i,int(request.form["DIMAB"])),
           "RecetasPL[{}].DIM_B_Comp_A=(DINT){}".format(i,int(request.form["DIMBA"])),
           "RecetasPL[{}].DIM_B_Comp_B=(DINT){}".format(i,int(request.form["DIMBB"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_A=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEA"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_B=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEB"])),
           "RecetasPL[{}].AnchoPliego_Comp_A=(DINT){}".format(i,int(request.form["ANCHOPLIEGOA"])),
           "RecetasPL[{}].AnchoPliego_Comp_B=(DINT){}".format(i,int(request.form["ANCHOPLIEGOB"])),
           "RecetasPL[{}].CalibreCaliente_Comp_A=(REAL){}".format(i,float(request.form["CALIBRECALIENTEA"])),
           "RecetasPL[{}].CalibreCaliente_Comp_B=(REAL){}".format(i,float(request.form["CALIBRECALIENTEB"]))
         ]
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            lista.append(value)
    return lista

#############################################################################################################################
   
def cambiarReceta(host, request):
    lista = []
    i = int(request.form["RECETA"])
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client

    cambioTexto(host,i,"Medida",listaASCII(request.form["PLIEGODEGOMA"]))
    cambioTexto(host,i,"PliegoMesaAlta",listaASCII(request.form["PLIEGODEMESAALTA"]))
    escribirGreenTire(host,i,request.form["GREENTIRE"])
    escribirCompuesto(host,i,[request.form["COMPUESTOA"],request.form["COMPUESTOB"]])

    tags=[
           "RecetasPL[{}].PresionRodillo=(DINT){}".format(i,int(request.form["PRESIÓNDERODILLO"])),
           "RecetasPL[{}].VelocidadMax=(DINT){}".format(i,int(request.form["VELOCIDADMAXIMA"])),
           "RecetasPL[{}].DIM_A_Comp_A=(DINT){}".format(i,int(request.form["DIMAA"])),
           "RecetasPL[{}].DIM_A_Comp_B=(DINT){}".format(i,int(request.form["DIMAB"])),
           "RecetasPL[{}].DIM_B_Comp_A=(DINT){}".format(i,int(request.form["DIMBA"])),
           "RecetasPL[{}].DIM_B_Comp_B=(DINT){}".format(i,int(request.form["DIMBB"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_A=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEA"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_B=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEB"])),
           "RecetasPL[{}].AnchoPliego_Comp_A=(DINT){}".format(i,int(request.form["ANCHOPLIEGOA"])),
           "RecetasPL[{}].AnchoPliego_Comp_B=(DINT){}".format(i,int(request.form["ANCHOPLIEGOB"])),
           "RecetasPL[{}].CalibreCaliente_Comp_A=(REAL){}".format(i,float(request.form["CALIBRECALIENTEA"])),
           "RecetasPL[{}].CalibreCaliente_Comp_B=(REAL){}".format(i,float(request.form["CALIBRECALIENTEB"]))
         ]
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            lista.append(value)
    return lista

#############################################################################################################################
   
def eliminarReceta(host, receta):
    lista = []
    i = int(receta)
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client

    cambioTexto(host,i,"Medida",listaASCII(""))
    cambioTexto(host,i,"PliegoMesaAlta",listaASCII(""))
    escribirGreenTire(host,i,"")
    escribirCompuesto(host,i,["",""])

    tags=[
           "RecetasPL[{}].PresionRodillo=(DINT){}".format(i,0),
           "RecetasPL[{}].VelocidadMax=(DINT){}".format(i,0),
           "RecetasPL[{}].DIM_A_Comp_A=(DINT){}".format(i,0),
           "RecetasPL[{}].DIM_A_Comp_B=(DINT){}".format(i,0),
           "RecetasPL[{}].DIM_B_Comp_A=(DINT){}".format(i,0),
           "RecetasPL[{}].DIM_B_Comp_B=(DINT){}".format(i,0),
           "RecetasPL[{}].AnchoSqueegee_Comp_A=(DINT){}".format(i,0),
           "RecetasPL[{}].AnchoSqueegee_Comp_B=(DINT){}".format(i,0),
           "RecetasPL[{}].AnchoPliego_Comp_A=(DINT){}".format(i,0),
           "RecetasPL[{}].AnchoPliego_Comp_B=(DINT){}".format(i,0),
           "RecetasPL[{}].CalibreCaliente_Comp_A=(REAL){}".format(i,0),
           "RecetasPL[{}].CalibreCaliente_Comp_B=(REAL){}".format(i,0)
         ]
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            lista.append(value)
    return lista

#############################################################################################################################
     
def escribirGreenTire(host,elemento,texto):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    
    greenTire = limpiatexto(texto)
    
    tags = []
    for indice, ASCII in enumerate(greenTire):
        for index, value in enumerate(ASCII):
            tags.append("RecetasPL[{}].GreenTire[{}].DATA[{}]=(SINT){}".format(elemento,indice,index,value))
        tags.append("RecetasPL[{}].GreenTire[{}].LEN=(DINT){}".format(elemento,indice,len(ASCII)))
        
    resultado = []
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            resultado.append(value)
        
    return resultado, tags

#############################################################################################################################
   
def leerGreenTire(host,indice):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    final = []
    tags = []
    val = []
    for i in range (6):
        tags.append("RecetasPL[{}].GreenTire[{}].LEN".format(indice,i))
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2):
            if value[0] != 0:
                val.append(str(value[0]))
    for index,value in enumerate(val):            
        valor = ["RecetasPL[{}].GreenTire[{}].Data[0-{}]".format(indice,index,value)]
        with connector( host=host ) as conn:
            for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( valor ), depth=2):
                final.append(value)
    
    greenTire = ""
    for i in range(len(final)):
        greenTire += listaSTRING(final[i]).strip("\x00")+", "

    return greenTire.strip(", ")

#############################################################################################################################
   
def leerCompuesto(host,indice):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    final = []
    tags = []
    val = []
    for i in range (4):
        tags.append("RecetasPL[{}].Compuesto[{}].LEN".format(indice,i)) 
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2):
            if value[0] != 0:
                val.append(value[0])       
    for index,value in enumerate(val):            
        valor = ["RecetasPL[{}].Compuesto[{}].Data[0-{}]".format(indice,index,value)]
        with connector( host=host ) as conn:
            for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( valor ), depth=2):
                final.append(value)    
    compuestos = []
    for i in range(len(final)):
        compuestos.append(listaSTRING(final[i]).strip("\x00"))
    return compuestos

#############################################################################################################################
  
def escribirCompuesto(host,elemento,texto):
    from cpppo.server.enip.client import connector
    from cpppo.server.enip import client
    
    greenTire = limpiatextoC(texto)
    
    tags = []
    for indice, ASCII in enumerate(greenTire):
        for index, value in enumerate(ASCII):
            tags.append("RecetasPL[{}].Compuesto[{}].DATA[{}]=(SINT){}".format(elemento,indice,index,value))
        tags.append("RecetasPL[{}].compuesto[{}].LEN=(DINT){}".format(elemento,indice,len(ASCII)))
        
    resultado = []
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            resultado.append(value)
        
    return resultado, tags

#############################################################################################################################

def exportarExcel(cnxn, output):
    import pandas as pd

    sql = "SELECT * FROM [squeegee].[dbo].[receta]"
    df = pd.read_sql(sql,cnxn)

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    formato = workbook.add_format()
    formato.set_bg_color('#eeeeee')
    worksheet.set_column(0,9,28)

    writer.close()
    output.seek(0)

    return output

#############################################################################################################################

def sincro_to_db(host, cursor, cnxn):
    
    listas = matriz(host)
    for lista in listas:
        sql = """UPDATE [squeegee].[dbo].[receta]
                SET [pliego_goma] = '{0}'
                    ,[pliego_mesa_alta] = '{1}'
                    ,[green_tire] = '{2}'
                    ,[presion_rodillo] = {3}
                    ,[velocidad_maxima] = {4}
                    ,[compuesto_a] = '{5}'
                    ,[calibre_caliente_a] = {6}
                    ,[ancho_squeegee_a] = {7}
                    ,[ancho_pliego_a] = {8}
                    ,[dima_a] = {9}
                    ,[dimb_a] = {10}
                    ,[compuesto_b] = '{11}'
                    ,[calibre_caliente_b] = {12}
                    ,[ancho_squeegee_b] = {13}
                    ,[ancho_pliego_b] = {14}
                    ,[dima_b] = {15}
                    ,[dimb_b] = {16}
                    ,[diferencia_yellow] = {17}
                    ,[diferencia_red] = {18}
                    ,[diferencia_blue] = {19}
                WHERE [id] = {20} """.format(
                lista[1],lista[2],lista[3],lista[4],lista[5],
                lista[6],lista[7],lista[8],lista[9],lista[10],lista[11], 
                lista[12],lista[13],lista[14],lista[15],lista[16],lista[17],
                lista[18],lista[19],lista[20],lista[0]
                )
        cursor.execute(sql) 
        cnxn.commit()
    print("carga lista")

#############################################################################################################################

def sincro_to_plc(host, cursor, cnxn):
    lista=[]
    cursor.execute("SELECT * FROM [squeegee].[dbo].[receta]")
    row = cursor.fetchone() 
    for z in range(1,300): 
        i = int(row[0])
        from cpppo.server.enip.client import connector
        from cpppo.server.enip import client

        cambioTexto(host,i,"Medida",listaASCII(row[1]))
        cambioTexto(host,i,"PliegoMesaAlta",listaASCII(row[2]))
        escribirGreenTire(host,i,row[3])
        escribirCompuesto(host,i,[row[6],row[12]])

        tags=[
            "RecetasPL[{}].PresionRodillo=(DINT){}".format(i,int(row[4])),
            "RecetasPL[{}].VelocidadMax=(DINT){}".format(i,int(row[5])),
            "RecetasPL[{}].DIM_A_Comp_A=(DINT){}".format(i,int(row[10])),
            "RecetasPL[{}].DIM_B_Comp_A=(DINT){}".format(i,int(row[11])),
            "RecetasPL[{}].DIM_A_Comp_B=(DINT){}".format(i,int(row[16])),
            "RecetasPL[{}].DIM_B_Comp_B=(DINT){}".format(i,int(row[17])),
            "RecetasPL[{}].AnchoSqueegee_Comp_A=(DINT){}".format(i,int(row[8])),
            "RecetasPL[{}].AnchoSqueegee_Comp_B=(DINT){}".format(i,int(row[14])),
            "RecetasPL[{}].AnchoPliego_Comp_A=(DINT){}".format(i,int(row[9])),
            "RecetasPL[{}].AnchoPliego_Comp_B=(DINT){}".format(i,int(row[15])),
            "RecetasPL[{}].CalibreCaliente_Comp_A=(REAL){}".format(i,float(row[7])),
            "RecetasPL[{}].CalibreCaliente_Comp_B=(REAL){}".format(i,float(row[13]))
            ]
        with connector( host=host ) as conn:
            for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
                lista.append(value)
        row = cursor.fetchone()
    print("carga lista")

#############################################################################################################################

def leer_db(cursor):
    lista=[]
    cursor.execute("SELECT * FROM [squeegee].[dbo].[historico] ORDER BY [fecha_modificacion] DESC ")
    row = cursor.fetchone() 
    while row:
        dt = row[21]
        fecha = "{}/{}/{} {}:{}:{}".format(dt.day,dt.month,dt.year,dt.hour,dt.minute,dt.second)
        value = {
            "i" : row[0],
            "medida" : row[1],
            "PliegoMesaAlta" : row[2],
            "GreenTire" : row[3],
            "Compuesto" : [row[6],row[12]],
            "PresionRodillo" : row[4],
            "VelocidadMax" : row[5],
            "dim_a_Comp_A" : row[10],
            "dim_b_Comp_A" : row[11],
            "dim_a_Comp_B" : row[16],
            "dim_b_Comp_B" : row[17],
            "AnchoSqueegee_Comp_A" : row[8],
            "AnchoSqueegee_Comp_B" : row[14],
            "AnchoPliego_Comp_A" : row[9],
            "AnchoPliego_Comp_B" : row[15],
            "CalibreCaliente_Comp_A" : row[7],
            "CalibreCaliente_Comp_B" : row[13],
            "diferencia_yellow" : row[18],
            "diferencia_red" : row[19],
            "diferencia_blue" : row[20],
            "fecha_modificacion" : fecha[0:23],
            "usuario" : row[22]
        }
        lista.append(value)
        row = cursor.fetchone()
    return lista

#############################################################################################################################

def inicio(cursor):
    lista=[]
    cursor.execute("SELECT * FROM [squeegee].[dbo].[receta]")
    row = cursor.fetchone() 
    while row: 
        yellow = int(row[17]) - int(row[11])
        red = yellow * 2 + int(row[14])
        blue = (int(row[15]) - red) / 2
        value = {
            "i" : row[0],
            "medida" : row[1],
            "PliegoMesaAlta" : row[2],
            "GreenTire" : row[3],
            "Compuesto" : [row[6],row[12]],
            "PresionRodillo" : row[4],
            "VelocidadMax" : row[5],
            "dim_a_Comp_A" : row[10],
            "dim_b_Comp_A" : row[11],
            "dim_a_Comp_B" : row[16],
            "dim_b_Comp_B" : row[17],
            "AnchoSqueegee_Comp_A" : row[8],
            "AnchoSqueegee_Comp_B" : row[14],
            "AnchoPliego_Comp_A" : row[9],
            "AnchoPliego_Comp_B" : row[15],
            "CalibreCaliente_Comp_A" : row[7],
            "CalibreCaliente_Comp_B" : row[13],
            "diferencia_yellow" : yellow,
            "diferencia_red" : red,
            "diferencia_blue" : blue,
            "fecha_modificacion" : row[21]
        }
        lista.append(value)
        row = cursor.fetchone()
    return lista

#############################################################################################################################

def leer_elemento(cursor, variable):
    cursor.execute("SELECT TOP 1 * FROM [squeegee].[dbo].[receta] WHERE [id] = {}".format(int(variable)))
    row = cursor.fetchone() 
    value = {
        "i" : row[0],
        "medida" : row[1],
        "PliegoMesaAlta" : row[2],
        "GreenTire" : row[3],
        "Compuesto" : [row[6],row[12]],
        "PresionRodillo" : row[4],
        "VelocidadMax" : row[5],
        "dim_a_Comp_A" : row[10],
        "dim_b_Comp_A" : row[11],
        "dim_a_Comp_B" : row[16],
        "dim_b_Comp_B" : row[17],
        "AnchoSqueegee_Comp_A" : row[8],
        "AnchoSqueegee_Comp_B" : row[14],
        "AnchoPliego_Comp_A" : row[9],
        "AnchoPliego_Comp_B" : row[15],
        "CalibreCaliente_Comp_A" : row[7],
        "CalibreCaliente_Comp_B" : row[13],
    }
    return value

#############################################################################################################################
    
def nuevaReceta_db(host, cursor, cnxn, request):
    receta = huecos(cursor)
    sql = """ UPDATE [squeegee].[dbo].[receta]
        SET [pliego_goma] = '{1}'
            ,[pliego_mesa_alta] = '{2}'
            ,[green_tire] = '{3}'
            ,[presion_rodillo] = {4}
            ,[velocidad_maxima] = {5}
            ,[compuesto_a] = '{6}'
            ,[calibre_caliente_a] = {7}
            ,[ancho_squeegee_a] = {8}
            ,[ancho_pliego_a] = {9}
            ,[dima_a] = {10}
            ,[dimb_a] = {11}
            ,[compuesto_b] = '{12}'
            ,[calibre_caliente_b] = {13}
            ,[ancho_squeegee_b] = {14}
            ,[ancho_pliego_b] = {15}
            ,[dima_b] = {16}
            ,[dimb_b] = {17}
        WHERE [id] = {0}""".format( 
        receta, 
        request.form["PLIEGODEGOMA"], 
        request.form["PLIEGODEMESAALTA"],
        request.form["GREENTIRE"],
        float(request.form["PRESIÓNDERODILLO"]), 
        float(request.form["VELOCIDADMAXIMA"]), 
        request.form["COMPUESTOA"],
        request.form["CALIBRECALIENTEA"],
        float(request.form["ANCHOSQUEEGEEA"]), 
        float(request.form["ANCHOPLIEGOA"]),
        float(request.form["DIMAA"]),
        float(request.form["DIMBA"]),
        request.form["COMPUESTOB"],
        request.form["CALIBRECALIENTEB"],
        float(request.form["ANCHOSQUEEGEEB"]), 
        float(request.form["ANCHOPLIEGOB"]), 
        float(request.form["DIMAB"]), 
        float(request.form["DIMBB"])
        )
    cursor.execute(sql) 
    cnxn.commit()
    print("receta {} creada".format(receta))

#############################################################################################################################
   
def cambiarReceta_db(host, cursor, cnxn, request):

    sql = """ UPDATE [squeegee].[dbo].[receta]
        SET [pliego_goma] = '{1}'
            ,[pliego_mesa_alta] = '{2}'
            ,[green_tire] = '{3}'
            ,[presion_rodillo] = {4}
            ,[velocidad_maxima] = {5}
            ,[compuesto_a] = '{6}'
            ,[calibre_caliente_a] = {7}
            ,[ancho_squeegee_a] = {8}
            ,[ancho_pliego_a] = {9}
            ,[dima_a] = {10}
            ,[dimb_a] = {11}
            ,[compuesto_b] = '{12}'
            ,[calibre_caliente_b] = {13}
            ,[ancho_squeegee_b] = {14}
            ,[ancho_pliego_b] = {15}
            ,[dima_b] = {16}
            ,[dimb_b] = {17}
        WHERE [id] = {0}""".format( 
        request.form["RECETA"], 
        request.form["PLIEGODEGOMA"], 
        request.form["PLIEGODEMESAALTA"],
        request.form["GREENTIRE"],
        float(request.form["PRESIÓNDERODILLO"]), 
        float(request.form["VELOCIDADMAXIMA"]), 
        request.form["COMPUESTOA"],
        request.form["CALIBRECALIENTEA"],
        float(request.form["ANCHOSQUEEGEEA"]), 
        float(request.form["ANCHOPLIEGOA"]),
        float(request.form["DIMAA"]),
        float(request.form["DIMBA"]),
        request.form["COMPUESTOB"],
        request.form["CALIBRECALIENTEB"],
        float(request.form["ANCHOSQUEEGEEB"]), 
        float(request.form["ANCHOPLIEGOB"]), 
        float(request.form["DIMAB"]), 
        float(request.form["DIMBB"])
        )
    cursor.execute(sql) 
    cnxn.commit()
    print("cambio listo")

#############################################################################################################################
   
def eliminarReceta_db(cursor, cnxn, receta):
    sql = """ UPDATE [squeegee].[dbo].[receta]
        SET [pliego_goma] = '{1}'
            ,[pliego_mesa_alta] = '{2}'
            ,[green_tire] = '{3}'
            ,[presion_rodillo] = {4}
            ,[velocidad_maxima] = {5}
            ,[compuesto_a] = '{6}'
            ,[calibre_caliente_a] = {7}
            ,[ancho_squeegee_a] = {8}
            ,[ancho_pliego_a] = {9}
            ,[dima_a] = {10}
            ,[dimb_a] = {11}
            ,[compuesto_b] = '{12}'
            ,[calibre_caliente_b] = {13}
            ,[ancho_squeegee_b] = {14}
            ,[ancho_pliego_b] = {15}
            ,[dima_b] = {16}
            ,[dimb_b] = {17}
        WHERE [id] = {0}""".format(receta, 
        '','',',,,,',0,0,'0',0,0,0,0,0,'0',0,0,0,0,0)
    cursor.execute(sql) 
    cnxn.commit()
    print("receta {} eliminada".format(receta))

#############################################################################################################################

def usuario(cursor):
    valores = {}
    cursor.execute("SELECT * FROM [squeegee].[dbo].[usuario]")
    row = cursor.fetchone() 
    while row: 
        value = [row[1],row[2], row[3]]
        valores[row[0]] = value
        row = cursor.fetchone()
    return valores

#############################################################################################################################

def tolerancia(cursor):
    cursor.execute("SELECT * FROM [squeegee].[dbo].[tolerancia]")
    row = cursor.fetchone()
    valores = {
        "calibre":row[0],
        "presion":row[1],
        "squeegee":row[2],
        "pliego":row[3],
        "dima":row[4],
        "dimb":row[5]
    }
    return valores

#############################################################################################################################
   
def cambiarTolerancia(cursor, cnxn, request):

    sql = """UPDATE [squeegee].[dbo].[tolerancia]
            SET [calibre_caliente] = {0}
                ,[presion_de_rodillo] = {1}
                ,[ancho_squeegee] = {2}
                ,[ancho_pliego] = {3}
                ,[dim_a] = {4}
                ,[dim_b] = {5}""".format( 
        request.form["CALIBRECALIENTE"],
        float(request.form["PRESIONDERODILLO"]), 
        float(request.form["ANCHOSQUEEGEE"]), 
        float(request.form["ANCHOPLIEGO"]), 
        float(request.form["DIMA"]), 
        float(request.form["DIMB"])
        )
    cursor.execute(sql) 
    cnxn.commit()
    print("cambio listo")

#############################################################################################################################

def huecos(cursor):
    cursor.execute("SELECT MIN([id]) FROM [squeegee].[dbo].[receta] WHERE [pliego_goma] = ''")
    row = cursor.fetchone()
    return row[0]

#############################################################################################################################

def insert(cursor, cnxn, request, session):

    # Campos estandar
    pliego_goma = request.form["PLIEGODEGOMA"]
    pliego_mesa_alta = request.form["PLIEGODEMESAALTA"]
    green_tire = request.form["GREENTIRE"]
    presion_rodillo = float(request.form["PRESIÓNDERODILLO"])
    velocidad_maxima = float(request.form["VELOCIDADMAXIMA"])

    # Campos del compuesto A
    compuesto_a = request.form["COMPUESTOA"]
    calibre_caliente_a = float(request.form["CALIBRECALIENTEA"])
    ancho_squeegee_a = float(request.form["ANCHOSQUEEGEEA"])
    ancho_pliego_a = float(request.form["ANCHOPLIEGOA"])
    dima_a = float(request.form["DIMAA"])
    dimb_a = float(request.form["DIMBA"])

    # Campos del compuesto B
    compuesto_b = request.form["COMPUESTOB"]
    calibre_caliente_b = float(request.form["CALIBRECALIENTEB"])
    ancho_squeegee_b = float(request.form["ANCHOSQUEEGEEB"])
    ancho_pliego_b = float(request.form["ANCHOPLIEGOB"])
    dima_b = float(request.form["DIMAB"])
    dimb_b = float(request.form["DIMBB"])

    # Diferencias
    diferencia_yellow = dimb_b - dimb_a
    diferencia_red = diferencia_yellow * 2 + ancho_squeegee_b
    diferencia_blue = (ancho_pliego_b - diferencia_red) / 2

    # usuario
    usuario = session["user"]

    sql = """INSERT INTO [squeegee].[dbo].[historico]
           ([pliego_goma],[pliego_mesa_alta],[green_tire],[presion_rodillo],[velocidad_maxima]
           ,[compuesto_a],[calibre_caliente_a],[ancho_squeegee_a],[ancho_pliego_a],[dima_a],[dimb_a]
           ,[compuesto_b],[calibre_caliente_b],[ancho_squeegee_b],[ancho_pliego_b],[dima_b],[dimb_b]
           ,[diferencia_yellow],[diferencia_red],[diferencia_blue],[usuario])
        VALUES
           ('{0}','{1}','{2}',{3},{4},
           '{5}',{6},{7},{8},{9},{10},
           '{11}',{12},{13},{14},{15},{16},
           {17},{18},{19},'{20}')""".format(
            pliego_goma,pliego_mesa_alta,green_tire,presion_rodillo,velocidad_maxima,
            compuesto_a,calibre_caliente_a,ancho_squeegee_a,ancho_pliego_a,dima_a,dimb_a,
            compuesto_b,calibre_caliente_b,ancho_squeegee_b,ancho_pliego_b,dima_b,dimb_b,
            diferencia_yellow,diferencia_red,diferencia_blue,usuario)
    


    cursor.execute(sql) 
    cnxn.commit()

#############################################################################################################################

def cargado(cursor, cnxn, session):

    usuario = session["user"]

    sql = """INSERT INTO [squeegee].[dbo].[historico]
           ([pliego_goma],[pliego_mesa_alta],[green_tire],[presion_rodillo],[velocidad_maxima]
           ,[compuesto_a],[calibre_caliente_a],[ancho_squeegee_a],[ancho_pliego_a],[dima_a],[dimb_a]
           ,[compuesto_b],[calibre_caliente_b],[ancho_squeegee_b],[ancho_pliego_b],[dima_b],[dimb_b]
           ,[diferencia_yellow],[diferencia_red],[diferencia_blue],[usuario])
        VALUES
           ('Carga a PLC realizada con exito','0','0',0,0,
           '0',0,0,0,0,0,
           '0',0,0,0,0,0,
           0,0,0,'{}')""".format(usuario)
    
    cursor.execute(sql) 
    cnxn.commit()

#############################################################################################################################

def sincronia(cursor):
    cursor.execute("SELECT TOP 1 [pliego_goma] FROM [squeegee].[dbo].[historico] ORDER BY [fecha_modificacion] DESC ")
    row = cursor.fetchone()
    if row[0] == 'Carga a PLC realizada con exito':
        return True
    else:
        return False