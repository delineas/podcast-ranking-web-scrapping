from bs4 import BeautifulSoup
from pprint import pprint


def buildContentObject(titleText, childText):
    contentObject = {
        'title': titleText.replace('[editar]',''),
        'anchor': childText
    }
    return contentObject


def spanWithId(tag):
    # Si el tag tiene un id entonces nos servirá para añadirlo a la lista toc
    return tag.name == 'span' and tag.has_attr('id')


# Primero debemos definir la función para luego llamarla
def extract_toc(filepath, body_class='#mw-content-text h3'):
    """
        Extrae el TOC de un fichero HTML almacenado en local proviniente de la wikipedia
        Devuelve una lista de items diccionario con title y anchor
    """
    try:
        file = open(filepath)
    except FileNotFoundError:
        print("El fichero no existe") 
    
    fileRead = file.read()

    soup = BeautifulSoup(fileRead, features="lxml")

    # TOC es una lista
    toc = []
    # Los titulos del contenido estan en este selector
    titles = soup.select(body_class)

    #breakpoint()

    for title in titles:
        # Leemos los datos hijos de titles (el HTML contiene el ID del anchor)
        # BeautifulSoup nos permite buscar dentro de una selección
        spans = title.findAll(spanWithId)
        
        for span in spans:
            
            childText = span.get('id')
            titleText = title.getText()
            contentObject = buildContentObject(titleText, childText=childText)
            toc.append(contentObject)

    return toc


pprint(extract_toc("sandbox/content/paella.html"))
