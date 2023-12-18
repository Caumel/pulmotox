from flask import Flask, render_template, request, jsonify
import requests
import os
import json
from src.cima import cima_api as cimaAPI
from src.umls import umls_api as umlsAPI
from src import utils as utils
from src import utils_clean_text as utils_clean_text


from bs4 import BeautifulSoup
import re

import spacy
import re

cima = cimaAPI.MyCimaAPI()
umls = umlsAPI.MyUmlsAPI()

template_dir = os.path.abspath('src/web')
app = Flask(__name__, template_folder=template_dir)

cima_url = os.getenv('CIMAL_URL', 'https://cima.aemps.es/cima/rest/')
timeout_value = int(os.getenv('TIMEOUT', 10))
path_words = "data/lista_nombre.txt"
path_pactivos = "data/nombres_pactivo_2023-12-16 07:58:33.txt"
names_medicamentos = None
pactivos = None


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

    p_activo = utils.seach_for_p_activo(pactivos,nregistro)

    results = []
    lines = utils_clean_text.clean_section_4_8(text[0]["contenido"])
    split_list = utils_clean_text.split_by_pactivo(lines,p_activo)
    for element in split_list:
        trastornos, texto_general = utils_clean_text.extract_trastornos(element)
        texto_umls = utils_clean_text.prepare_texto_para_buscar_reacciones_adversas(texto_general)
        text_analizado = utils.search_reacciones_adversas(texto_umls,umls)

        results.append([trastornos,text_analizado])
    
    return results

@app.route('/seach_process', methods=['POST'])
def seach_process():
    text = request.json['text']
    result = seach_process_function(text)
    return jsonify(result)

if __name__ == '__main__':
    names_medicamentos = utils.read_names_medicamentos(path_words)
    pactivos = utils.get_med_nregistro_name(path_pactivos)
    # Leer todos los p activos
    app.run(debug=True) 