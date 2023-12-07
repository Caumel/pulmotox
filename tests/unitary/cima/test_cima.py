import pandas as pd
import numpy as np
import shutil
import os
from pathlib import Path
from datetime import datetime
import time
import threading
import json
import urllib
import requests
import hashlib
import pytest
from src.cima import cima_api as API


cima_url = os.getenv('CIMAL_URL', 'https://cima.aemps.es/cima/rest/')
timeout_value = int(os.getenv('TIMEOUT', 10))


def md5(fname):
    """Funcion para calcular el valor md5 de un archivo

    Args:
        fname (str): Nombre del archivo a calcular

    Retorna:
        str: Valor md5 del archivo
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@pytest.fixture
def api():
    """Funcion para instanciar una api de Sentinel

    Retorna:
        MySentinelAPI: Instancia sentinel api
    """
    return API.MyCimaAPI()

def test_create_url(api):
    dic_var = {
        "nombre": "nombre" 
    }
    kind = "medicamentos?"
    url_method = api.create_url(kind,dic_var)
    url = "https://cima.aemps.es/cima/rest/medicamentos?&nombre=nombre"
    assert url_method == url
def test_get_medicamentos(api):
    name = "EUTIROX"
    reponse, code = api.get_medicamentos(name=name)

    assert reponse["totalFilas"] == 11 \
            and reponse["pagina"] == 1 \
            and reponse["resultados"][0]["nregistro"] == "64014" \
            and reponse["resultados"][0]["nombre"] == "EUTIROX 100 microgramos COMPRIMIDOS" \
            and reponse["resultados"][10]["nregistro"] == "70044" \
            and reponse["resultados"][10]["nombre"] == "EUTIROX 88 microgramos COMPRIMIDOS" \
            and code == 200

def test_get_medicamentos_all(api):
    name = "EUTIROX"
    list_objects = api.get_medicamentos_all(name=name)

    assert len(list_objects) == 11 \
            and list_objects[0]["nregistro"] == "64014" \
            and list_objects[0]["nombre"] == "EUTIROX 100 microgramos COMPRIMIDOS" \
            and list_objects[-1]["nregistro"] == "70044" \
            and list_objects[-1]["nombre"] == "EUTIROX 88 microgramos COMPRIMIDOS" \

def test_get_medicamento(api):
    name = "EUTIROX"
    text, resp_code = api.get_medicamento(nregister=64014)
    print(text)

    assert resp_code == 200 \
            and text["nregistro"] == "64014" \
            and text["nombre"] == "EUTIROX 100 microgramos COMPRIMIDOS" \
            and text["pactivos"] == "LEVOTIROXINA SODICA" \

# def test_get_info_medicamento_section(api):
#     pass
# def test_get_info_secciones(api):
#     pass
# def test_buscarEnFichaTecnica(api):
#     pass
# def test_registroCambios(api):
#     pass