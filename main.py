from flask import Flask, request, render_template
import requests
import os
import json
from src.cima import cima_api as cimaAPI
from src import utils as utils

cima = cimaAPI.MyCimaAPI()

template_dir = os.path.abspath('src/web')
app = Flask(__name__, template_folder=template_dir)

cima_url = 'https://cima.aemps.es/cima/rest/'
timeout_value = 10

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_word = request.form['search']
        # Call your method here with search_word
        result = your_method(search_word)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

def your_method(word):
    list_elements = cima.get_medicamentos_all(name=word)
    nregistro = list_elements[0]["nregistro"]
    text, status = cima.get_info_medicamento_section(typeDoc=1,nregister=nregistro,section="4.8")

    text_prety = utils.extract_and_clean_text(text)

    return f"{word ,text_prety}"

if __name__ == '__main__':
    app.run(debug=True)