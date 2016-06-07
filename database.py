import pymongo

def read():
    try:
        conexion = pymongo.MongoClient()
        print " * Conexion con MongoDB correcta..."
    except pymongo.errors.ConnectionFailure, e:
        print "No se ha podido conectar a mongoDB: %s" % e

    BD = conexion['visitasSD']
    coleccion = BD.secciones

    lista = [['seccion', 'visitas']]

    ultima = coleccion.find()[coleccion.find().count() - 1]

    dicc = {
                'tecnologia': ultima['tecnologia'],
                'deportes': ultima['deportes'],
                'economia': ultima['economia'],
                'politica': ultima['politica'],
                'ciencia': ultima['ciencia']
    }

    return dicc

def write(datos):
    try:
        conexion = pymongo.MongoClient()
    except pymongo.errors.ConnectionFailure, e:
        print "No se ha podido conectar a mongoDB: %s" % e

    BD = conexion['visitasSD']
    coleccion = BD.secciones
    doc = {'tecnologia': datos['tecnologia'],
            'deportes': datos['deportes'],
            'economia': datos['economia'],
            'politica': datos['politica'],
            'ciencia': datos['ciencia']
            }
    coleccion.insert(doc)
    print " * Se han insertado los datos en MongoDB correctamente...Yuju (por fin)"
