#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import lxml.html
import feedparser
import threading
import time
import tweepy
import requests.packages.urllib3
from feeds_aux import *
from random import randint
import json
from database import *

requests.packages.urllib3.disable_warnings()

# ================================================= #
# URLS FEEDS
# ================================================= #

URLs_Tecnologia = {'http://feeds.weblogssl.com/xatakandroid': 'XatakaAndroid',
                    'http://feeds.weblogssl.com/xataka2': 'XatakaApple'
                    }

URLs_Deportes = {'http://feeds.weblogssl.com/motorpasion': 'XatakaMotor',
                    'http://elpais.com/tag/rss/futbol/a/': 'EL PAIS',
                    'http://www.abc.es/rss/feeds/abc_Deportes.xml':'ABC'
                    }

URLs_Economia = {'http://www.abc.es/rss/feeds/abc_Economia.xml':'ABC',
                    'http://estaticos.elmundo.es/elmundo/rss/economia.xml':'EL MUNDO'
                    }

URLs_Politica = {'http://www.elperiodico.com/es/rss/politica/rss.xml':'El periodico',
                    'http://estaticos.expansion.com/rss/economiapolitica.xml':'Expansion',
                    }

URLs_Ciencia = {'http://feeds.weblogssl.com/xatakaciencia': 'XatakaCiencia'}

# ================================================ #
# IMAGEN PREDETERMINADA
# ================================================ #

sin_imagen = {'tecnologia':'http://1.bp.blogspot.com/-q1NeBdQRkwU/UJAAhw0W9eI/AAAAAAAABeI/vO65uf9c4sA/s1600/13.fondos-gratis-de-vectores-abstractos.jpg',
              'deportes' : 'http://guiafitness.com/wp-content/uploads/fitness_background.jpg',
              'economia' : 'http://www.verportugal.net/vp/images/cms-image-000004651.jpg',
              'politica' : 'http://img.vavel.com/articulo-foto-2-8274262133.gif',
              'ciencia' : 'http://www.juventudtecnica.cu/sites/default/files/materiales%20periodisticos/ciencia2014.jpg'
              }

# ================================================= #
# LECTURA DE FEEDS
# =================================================#

dict_tecno = {}
dict_deportes = {}
dict_economia = {}
dict_politica = {}
dict_ciencia = {}

def LeerFeds():
    global dict_tecno
    global dict_deportes
    global dict_economia
    global dict_politica
    global dict_ciencia
    while(True):
        dict_tecno = parse_feeds(URLs_Tecnologia, sin_imagen['tecnologia'])
        print " * Feeds Tecnologia..... OK"

        dict_deportes = parse_feeds(URLs_Deportes, sin_imagen['deportes'])
        print " * Feeds Deportes....... OK"

        dict_economia = parse_feeds(URLs_Economia, sin_imagen['economia'])
        print " * Feeds Economia....... OK"

        dict_politica = parse_feeds(URLs_Politica, sin_imagen['politica'])
        print " * Feeds Politica....... OK"

        dict_ciencia = parse_feeds(URLs_Ciencia, sin_imagen['ciencia'])
        print " * Feeds Ciencia........ OK"
        print "............................\n"
        time.sleep(600)
        print " ** Lectura de nuevos feeds **"
        print "..............................."
    return

Lector = threading.Thread(target = LeerFeds)

Lector.start()

# ================================================= #
# REDES SOCIALES
# ================================================= #

# Keys twitter

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Keys facebook

def RedesSociales():
    while(True):
        time.sleep(15)
        dicts = {1:dict_tecno, 2:dict_deportes, 3:dict_economia, 4:dict_politica, 5:dict_ciencia}
        r = randint(1,5)
        ultima_noticia = {'titulo':dicts[r]['titulos'][0], 'link':dicts[r]['links'][0], 'fecha':dicts[r]['fechas'][0],
        'fuente':dicts[r]['fuentes'][0], 'imagen':dicts[r]['imagenes']}
        try:
            s = add_hash_tag(ultima_noticia['titulo'])
            api.update_status(s + "\n\n" + ultima_noticia['link'])
            print " * Tweet enviado"
        except:
            print " * Tweet repetido"
        time.sleep(1800)
    return

Redes = threading.Thread(target = RedesSociales)

Redes.start()

# ================================================ #
# Hilo que se encarga de almacenar en un fichero
# ================================================ #

DATOS = {}

def Estadisticas():
    global DATOS
    DATOS = read()

    print " ** Recuperando estadisticas **"
    print " ------------------------------"
    print " * Tecnologia: " + str(DATOS['tecnologia'])
    print " * Deportes: " + str(DATOS['deportes'])
    print " * Economia: " + str(DATOS['economia'])
    print " * Politica: " + str(DATOS['politica'])
    print " * Ciencia: " + str(DATOS['ciencia'])
    print " ------------------------------"

    while(True):
        time.sleep(120)
        write(DATOS)
    return

Fichero = threading.Thread(target = Estadisticas)

Fichero.start()

# ================================================= #
# APLICACION FLASK
# ================================================= #

app = Flask(__name__)

@app.route("/")
def home():
    return render_template( "home.html",
                            T_T = dict_tecno['titulos'][:2], F_T = dict_tecno['fuentes'][:2],
                            T_D = dict_deportes['titulos'][:2], F_D = dict_deportes['fuentes'][:2],
                            T_E = dict_economia['titulos'][:2], F_E = dict_economia['fuentes'][:2],
                            T_P = dict_politica['titulos'][:2], F_P = dict_politica['fuentes'][:2],
                            T_C = dict_ciencia['titulos'][:2], F_C = dict_ciencia['fuentes'][:2]
                            )

# ================================================= #

@app.route("/tecnologia")
def tecnologia():
    global DATOS
    DATOS['tecnologia'] += 1
    return render_template("tecnologia.html",
                            Titulares = dict_tecno['titulos'][:30],
                            Links = dict_tecno['links'][:30],
                            Fuentes = dict_tecno['fuentes'][:30],
                            Imagenes = dict_tecno['imagenes'][:30],
                            N = 10
                            )

# ================================================= #

@app.route("/deportes")
def deportes():
    global DATOS
    DATOS['deportes'] += 1
    return render_template("deportes.html",
                            Titulares = dict_deportes['titulos'][:30],
                            Links = dict_deportes['links'][:30],
                            Fuentes = dict_deportes['fuentes'][:30],
                            Imagenes = dict_deportes['imagenes'][:30],
                            N = 10
                            )

# ================================================= #

@app.route("/economia")
def economia():
    global DATOS
    DATOS['economia'] += 1
    return render_template("economia.html",
                            Titulares = dict_economia['titulos'][:30],
                            Links = dict_economia['links'][:30],
                            Fuentes = dict_economia['fuentes'][:30],
                            Imagenes = dict_economia['imagenes'][:30],
                            N = 10
                            )

# ================================================= #

@app.route("/politica")
def politica():
    global DATOS
    DATOS['politica'] += 1
    return render_template("politica.html",
                            Titulares = dict_politica['titulos'][:30],
                            Links = dict_politica['links'][:30],
                            Fuentes = dict_politica['fuentes'][:30],
                            Imagenes = dict_politica['imagenes'][:30],
                            N = 10
                            )

# ================================================= #

@app.route("/ciencia")
def ciencia():
    global DATOS
    DATOS['ciencia'] += 1
    return render_template("ciencia.html",
                            Titulares = dict_ciencia['titulos'][:30],
                            Links = dict_ciencia['links'][:30],
                            Fuentes = dict_ciencia['fuentes'][:30],
                            Imagenes = dict_ciencia['imagenes'][:30],
                            N = 10
                            )

@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html",
                            TECNO = DATOS['tecnologia'],
                            DEPOR = DATOS['deportes'],
                            ECONO = DATOS['economia'],
                            POLI = DATOS['politica'],
                            CIEN = DATOS['ciencia'],
                            )

# ================================================= #

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 32040, threaded = True)