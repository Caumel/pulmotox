from flask import Flask, render_template, request, jsonify
import requests
import os
import json
from src.cima import cima_api as cimaAPI
from src import utils as utils

cima = cimaAPI.MyCimaAPI()

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
    text_prety = utils.extract_and_clean_text(text[0]["contenido"])
    return f"{text_prety}"

@app.route('/seach_process', methods=['POST'])
def seach_process():
    text = request.json['text']
    result = seach_process_function(text)
    return jsonify(result)

if __name__ == '__main__':
    names_medicamentos = read_words(path_words)
    app.run(debug=True)