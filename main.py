from flask import Flask, render_template, request, jsonify
import requests
import os
import json
from src.cima import cima_api as cimaAPI
from src.umls import umls_api as umlsAPI
from src import utils as utils

from bs4 import BeautifulSoup
import re

import spacy
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from tqdm import tqdm

nltk.download('stopwords')

cima = cimaAPI.MyCimaAPI()
umls = umlsAPI.MyUmlsAPI()

template_dir = os.path.abspath('src/web')
app = Flask(__name__, template_folder=template_dir)

cima_url = os.getenv('CIMAL_URL', 'https://cima.aemps.es/cima/rest/')
timeout_value = int(os.getenv('TIMEOUT', 10))
path_words = "data/lista_nombre.txt"
names_medicamentos = None

def read_words(path):
    with open(path, 'r') as file:
        content = file.read()
    # Split the content by ':' and remove any whitespace
    names = [num.strip() for num in content.split(':')]
    return names

@app.route('/')
def index():
    return render_template('index.html')

def process_text(text):
    results = utils.suggest_word(text, names_medicamentos)
    plot = results if len(results)<5 else results[:5]
    lista_plot = []
    for index,result in enumerate(results):
        lista_plot.append(result)#[0] + ": " + str(result[1]) + " %")
    return lista_plot

@app.route('/process_text', methods=['POST'])
def process():
    text = request.json['text']
    result = process_text(text)
    return jsonify(result)

def seach_process_function(text):
    list_elements = cima.get_medicamentos_all(name=text)
    nregistro = list_elements[0]["nregistro"]
    text, status = cima.get_info_medicamento_section(typeDoc=1,nregister=nregistro,section="4.8")

    listas_filtradas = get_clean_text(text[0]["contenido"])
    print("lista_filtrada")
    lista_reacciones_adversas = search_reacciones_adversas(listas_filtradas)
    print("lista_reacciones")
    return lista_reacciones_adversas


# TODO: Este metodo es demasiado basto, esta puesto asi para el ejemplo.
def get_clean_text(texto):

    stop_words = set(stopwords.words('spanish'))

    html_content = texto
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text and filter out empty lines
    text = soup.get_text(separator='\n').strip()
    cleaned_text = re.sub(r'\xa0', '', text)

    lines = re.split(r'\n{2,}', cleaned_text)
    for index,element in enumerate(lines):
        cleaned_text = re.sub(r'\n', '', element)
        lines[index] = cleaned_text

    cleaned_text = '\n'.join(lines)

    low_not_dots = ''.join([char for char in cleaned_text.lower() if char != '.'])
    low_not_dots

    a = low_not_dots.split("\n")

    b = re.sub(':', '', low_not_dots)
    texto = b.split("\n")

    new_texto = []
    for linea in texto:
        linea_limpia = utils.limpiar_texto(linea)
        linea_lematizada = utils.lematizar_texto(linea_limpia)
        tokens = word_tokenize(linea_lematizada)
        new_texto.append(tokens)

    listas_filtradas = [[elemento for elemento in lista if elemento not in stop_words] for lista in new_texto]

    return listas_filtradas

def search_reacciones_adversas(texto_analizar):
    pairs = utils.get_pairs(texto_analizar)
    reacciones_adversas = []
    for pair in tqdm(pairs):
        text = pair[0] + " " + pair[1]
        response, code = umls.request_text_umls(text)
        # print(response["result"]["results"])
        if response["result"]["results"] is not None:
            for index,element in enumerate(response["result"]["results"]):
                # print(element["name"])
                reacciones_adversas.append(element["name"])
        else:
            continue
            # print("Not element found")
    return utils.remove_duplicated(reacciones_adversas)

@app.route('/seach_process', methods=['POST'])
def seach_process():
    text = request.json['text']
    result = seach_process_function(text)
    return jsonify(result)

if __name__ == '__main__':
    names_medicamentos = read_words(path_words)
    app.run(debug=True)