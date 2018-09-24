def listaASCII(texto):
    a = [ord(i) for i in texto]
    return a

def listaSTRING(ASCII):
    a = ''.join(chr(i) for i in ASCII)
    return a

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
            "Liner_Toegard_RedHMI",
            "Liner_Toegard_BlueHMI",
            "Liner_Toegard_YellowHMI",
            "RecetasPL[{}].DIM_A[0]".format(i),
            "RecetasPL[{}].DIM_A[1]".format(i),
            "RecetasPL[{}].DIM_B[0]".format(i),
            "RecetasPL[{}].DIM_B[1]".format(i),
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
    for l in range(0,299):
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

    tags=[
           "RecetasPL[{}].PresionRodillo=(DINT){}".format(i,int(request.form["PRESIÓNDERODILLO"])),
           "RecetasPL[{}].VelocidadMax=(DINT){}".format(i,int(request.form["VELOCIDADMAXIMA"])),
           "RecetasPL[{}].DIM_A[0]=(DINT){}".format(i,int(request.form["DIMBB"])),
           "RecetasPL[{}].DIM_A[1]=(DINT){}".format(i,int(request.form["DIMAA"])),
           "RecetasPL[{}].DIM_B[0]=(DINT){}".format(i,int(request.form["DIMBB"])),
           "RecetasPL[{}].DIM_B[1]=(DINT){}".format(i,int(request.form["DIMBA"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_B=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEB"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_A=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEA"])),
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

    tags=[
           "RecetasPL[{}].PresionRodillo=(DINT){}".format(i,int(request.form["PRESIÓNDERODILLO"])),
           "RecetasPL[{}].VelocidadMax=(DINT){}".format(i,int(request.form["VELOCIDADMAXIMA"])),
           "RecetasPL[{}].DIM_A[0]=(DINT){}".format(i,int(request.form["DIMBB"])),
           "RecetasPL[{}].DIM_A[1]=(DINT){}".format(i,int(request.form["DIMAA"])),
           "RecetasPL[{}].DIM_B[0]=(DINT){}".format(i,int(request.form["DIMBB"])),
           "RecetasPL[{}].DIM_B[1]=(DINT){}".format(i,int(request.form["DIMBA"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_B=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEB"])),
           "RecetasPL[{}].AnchoSqueegee_Comp_A=(DINT){}".format(i,int(request.form["ANCHOSQUEEGEEA"])),
           "RecetasPL[{}].AnchoPliego_Comp_A=(DINT){}".format(i,int(request.form["ANCHOPLIEGOA"])),
           "RecetasPL[{}].AnchoPliego_Comp_B=(DINT){}".format(i,int(request.form["ANCHOPLIEGOB"])),
           "RecetasPL[{}].CalibreCaliente_Comp_A=(REAL){}".format(i,float(request.form["CALIBRECALIENTEA"])),
           "RecetasPL[{}].CalibreCaliente_Comp_B=(REAL){}".format(i,float(request.form["CALIBRECALIENTEB"]))
         ]
    with connector( host=host ) as conn:
        for index,descr,op,reply,status,value in conn.pipeline(operations=client.parse_operations( tags ), depth=2 ):
            lista.append(value)
    return lista