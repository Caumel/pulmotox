import os
import string
import copy
import unicodedata

from bs4 import BeautifulSoup
import spacy
import re

nlp = spacy.load('es_core_news_sm')

##########################
#                        #
#  Clean html and split  #
#                        #
##########################

def remove_puntuation_sign(text):
    """
    Elimina los signos de puntuación de una cadena de texto.
    
    Input:
    - text (String): Cadena de texto de la que se eliminarán los signos de puntuación.
    
    Output:
    - (String): Cadena de texto sin signos de puntuación.
    """
    return ''.join(char for char in text if char not in string.punctuation)

def replace_element(text,be_replace,replace):
    """
    Reemplaza todas las ocurrencias de una subcadena por otra en un texto dado.

    Input:
    - text (String): Texto en el que se realizarán los reemplazos.
    - be_replace (String): Subcadena que será reemplazada.
    - replace (String): Subcadena con la que se reemplazará.

    Output:
    - (String): Texto modificado con los reemplazos realizados.
    """
    return re.sub(be_replace, replace, text)

def transform_html_to_text(html_content):
    """
    Convierte contenido HTML en texto plano, preservando saltos de línea.

    Input:
    - html_content (String): Contenido HTML en formato de cadena de texto.

    Output:
    - (String): Texto plano derivado del contenido HTML.
    """
    text = BeautifulSoup(html_content, 'html.parser')
    return text.get_text(separator='\n').strip()

def split_texto(by_what,text):
    """
    Divide un texto en una lista, utilizando una expresión regular como delimitador.

    Input:
    - by_what (String): Expresión regular que se usará como delimitador.
    - text (String): Texto que se dividirá.

    Output:
    - (List): Lista de cadenas resultantes de la división del texto.
    """
    return re.split(by_what, text)

def remove_jump_text_html(text):
    """
    Limpia un texto HTML eliminando caracteres específicos y dividiéndolo en partes.

    Input:
    - text (String): Texto HTML en formato de cadena.

    Output:
    - (List): Lista de partes del texto, limpiado y dividido según criterios específicos.
    """
    cleaned_text = replace_element(text,r'\xa0', '')
    return split_texto(r'\n{2,}', cleaned_text)

def split_given_a_list_all(lines,lista):
    """
    Divide cada elemento de una lista de líneas de texto, basado en si contienen elementos de otra lista.
    Si una línea contiene algún elemento de 'lista', se divide por ':' y se quitan espacios en blanco.

    Input:
    - lines (List): Lista de líneas de texto.
    - lista (List): Lista de elementos para comprobar en cada línea.

    Output:
    - new_lines (List): Lista de líneas divididas y procesadas.
    """
    new_lines = []
    for element in lines:
        if any(frecuencia in element for frecuencia in lista):
            resultado = [parte.strip() for parte in element.split(":") if parte.strip()]
        else:
            resultado = [element]
        new_lines = save_resultado_in_list(new_lines,resultado)
    return new_lines

def save_resultado_in_list(lista,resultado):
    """
    Agrega cada elemento de una lista de resultados a otra lista.

    Input:
    - lista (List): Lista a la que se agregarán elementos.
    - resultado (List): Lista de elementos a agregar.

    Output:
    - lista (List): Lista actualizada con elementos agregados.
    """
    for element_of_resultado in resultado:
        lista.append(element_of_resultado)
    return lista

def join_frecuencias(lista):
    """
    Une líneas en una lista si la siguiente línea comienza con '-', formando una única línea.

    Input:
    - lista (List): Lista de líneas de texto.

    Output:
    - lineas_unidas (List): Lista de líneas con algunas líneas unidas según el criterio especificado.
    """
    lineas_unidas = []
    i = 0
    while i < len(lista):
        if i + 1 < len(lista) and lista[i + 1].startswith('-'):
            lineas_unidas.append(lista[i] + " " + lista[i + 1].lstrip('-'))
            i += 2
        else:
            lineas_unidas.append(lista[i])
            i += 1
    return lineas_unidas

def clean_section_4_8(seccion_4_8):
    """
    Procesa una sección de texto (presumiblemente HTML), limpiándola y dividiéndola según ciertos criterios.

    Input:
    - seccion_4_8 (String): Texto HTML de la sección a procesar.

    Output:
    - lines_new (List): Lista de líneas de texto procesadas y divididas.
    """
    text = transform_html_to_text(seccion_4_8)
    lines = remove_jump_text_html(text)
    lines = join_frecuencias(lines)
    lines_new = [replace_element(line,r'\n','') for line in lines]
    lines_new = split_given_a_list_all(lines_new,["Trastornos"])
    return lines_new

def split_given_a_list(text,lista):
    """
    Divide una cadena de texto en una lista basada en la presencia de elementos de otra lista.
    Si algún elemento de 'lista' está en 'text', divide 'text' por ':'.

    Input:
    - text (String): Cadena de texto a dividir.
    - lista (List): Lista de elementos para buscar en 'text'.

    Output:
    - resultado (List): Lista de partes divididas de 'text'.
    """
    if any(frecuencia in text for frecuencia in lista):
        resultado = [parte.strip() for parte in text.split(":") if parte.strip()]
    else:
        resultado = [text]
    return resultado

##########################
#                        #
#    Split by pactivo    #
#                        #
##########################

def normalize(text):
    """
    Normaliza un texto: convierte a minúsculas, elimina puntuación y acentos, y ordena las palabras alfabéticamente.

    Input:
    - text (String): Cadena de texto a normalizar.

    Output:
    - (String): Texto normalizado.
    """
    # Convert to lower case
    text = text.lower()
    text = ''.join(char for char in text if char not in string.punctuation)
    # Normalize (remove accents)
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    # Split, sort and rejoin words
    return ' '.join(sorted(text.split()))

def are_texts_equivalent(text1, text2):
    """
    Compara dos textos para determinar si son equivalentes después de normalizarlos.

    Inputs:
    - text1 (String): Primer texto para comparar.
    - text2 (String): Segundo texto para comparar.

    Output:
    - (Boolean): Booleano indicando si los textos son equivalentes.
    """
    return normalize(text1) == normalize(text2)

# Function to split the lines based on the given criteria
def split_list_by_keywords(lines, pactivo):
    """
    Divide una lista de líneas de texto en secciones basadas en palabras clave.

    Inputs:
    - lines (List): Lista de líneas de texto.
    - pactivo (List): Lista de palabras clave.

    Output:
    - result (List): Lista de listas, cada una representando una sección del texto original.
    """
    # Initialize variables
    result = []
    current_section = []

    # Iterate through each line in the list
    for line in lines:
        # Check if the line contains any of the keywords
        if any(are_texts_equivalent(line, text) for text in pactivo):
            # If the current section is not empty, add it to the result
            if current_section:
                result.append(current_section)
                current_section = []
        # Add the line to the current section
        current_section.append(line)

    # Add the last section to the result
    if current_section:
        result.append(current_section)

    return result

def split_by_pactivo(lineas,pactivos_row):
    """
    Divide un conjunto de líneas de texto en secciones basadas en una lista de principios activos.

    Inputs:
    - lineas (List): Lista de líneas de texto a dividir.
    - pactivos_row (List): Cadena de texto con los principios activos separados por comas.

    Output:
    - (List): Lista de secciones de texto divididas según los principios activos.
    """
    split_by = "Notificación de sospechas de reacciones adversas"
    pactivo = pactivos_row.split(", ").copy()
    pactivo.append(split_by)

    # Split the list
    return split_list_by_keywords(lineas, pactivo)

##########################
#                        #
#   Split by trastorno   #
#                        #
##########################

def extract_trastornos(info):
    """
    Extrae y organiza información sobre trastornos y sus frecuencias a partir de un texto.

    Input:
    - info (List): Lista de líneas de texto que contienen información sobre trastornos.

    Output:
    - trastornos (Dict): Diccionario que organiza los trastornos por categorías y frecuencias.
    - texto_general (List): Lista de líneas de texto que no encajan en las categorías de trastornos.
    """

    trastornos = {}
    trastorno_actual = None
    frecuencia_actual = None
    first_visit_transtorno = False
    texto_general = []  # Para almacenar texto que no encaja en las otras categorías

    frecuencias = {'Frecuentes': [], 'Poco frecuentes': [], 'Raros': [], 'Raras': [], 'Muy raros': [], 'Muy raras':[], "Frecuencia no conocida": [], 'Sin especificar': []}
    lista_frecuencias = ['Frecuentes', 'Poco frecuentes', 'Raros', 'Raras', 'Muy raros','Muy raras',"Frecuencia no conocida"]

    for linea in info:
        if 'Trastornos' in linea:
            trastorno_actual = linea.split(':')[0]
            if not trastorno_actual in trastornos:
                trastornos[trastorno_actual] = copy.deepcopy(frecuencias)
            frecuencia_actual = 'Sin especificar'
            first_visit_transtorno = True
        elif any(frecuencia in linea for frecuencia in lista_frecuencias):
            frecuencia_actual = next(frec for frec in lista_frecuencias if frec in linea)
            text_split = split_given_a_list(linea,lista_frecuencias)
            trastornos[trastorno_actual][frecuencia_actual].append(text_split[-1])
            first_visit_transtorno = False
        elif first_visit_transtorno:
            trastornos[trastorno_actual][frecuencia_actual].append(linea)
            first_visit_transtorno = False
        else:
            texto_general.append(linea)  # Almacenar texto que no encaja en las otras categorías

    return trastornos, texto_general

##########################
#                        #
#   Prepare text umls    #
#                        #
##########################

def prepare_texto_para_buscar_reacciones_adversas(texto):
    """
    Prepara un texto para la búsqueda de reacciones adversas, realizando limpieza, tokenización,
    eliminación de stopwords y lematización.

    Input:
    - texto (List): Lista de líneas de texto a procesar.

    Output:
    - new_texto (List): Lista de listas, donde cada sublista contiene los lemas de las palabras no triviales 
      (no stopwords) de cada línea del texto original.
    """
    cleaned_text = '\n'.join(texto)

    texto_sin_puntuacion = ''.join(char for char in cleaned_text if char not in string.punctuation)

    texto = texto_sin_puntuacion.split("\n")

    # Procesar cada línea del texto
    new_texto = []
    for linea in texto:
        doc = nlp(linea)
        # Tokenizar, eliminar stopwords y lematizar
        listas_filtradas = [token.lemma_ for token in doc if not token.is_stop]
        new_texto.append(listas_filtradas)

    return new_texto