import lxml.html
import feedparser
import re

def parse_feeds (URLs, sin_imagen):
    lista = []
    for url in URLs:
        D = feedparser.parse(url)
        for item in D.entries:
            if item.published_parsed :
                linea = str(item['summary_detail'])
                match = re.search (r'http\S+.jpg', linea)
                nuevo = {
                    'titulo': item.title,
                    'link': item.link,
                    'fecha': item.published_parsed,
                    'fuente': URLs[url],
                    'imagen': match.group().split()[0] if match else sin_imagen
                }
                lista.append(nuevo)

    #ordenar el vector por fecha, la mas reciente primero
    lista.sort(key=lambda e: e['fecha'], reverse=True)




    dict_vectores = {'titulos':[noticia['titulo'] for noticia in lista],
                     'links': [noticia['link'] for noticia in lista],
                     'fechas': [noticia['fecha'] for noticia in lista],
                     'fuentes': [noticia['fuente'] for noticia in lista],
                     'imagenes': [noticia['imagen'] for noticia in lista]
                     }
    return dict_vectores

def add_hash_tag(s):
    indices = [i for i, c in enumerate(s) if c.isupper() and (s[i-1].isspace() or i == 0)]

    for i in range(len(indices)):
        s = s[:indices[i]] + "#" + s[indices[i]:]
        indices = [pos+1 for pos in indices]

    return s
