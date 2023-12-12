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

umls_url = os.getenv('UMLS_URL', 'https://uts-ws.nlm.nih.gov/rest')
umls_api_key = os.getenv('UMLS_API_KEY', '577c8f76-500d-4e94-9139-8a798bdbe78f')
timeout_value = int(os.getenv('TIMEOUT', 10))

class MyUmlsAPI:
    # TODO:

    """API para UMLS.

            Atributos
            ----------

            Constructor
            ------------
                MyUmlsAPI()

            Métodos
            -------
                create_url: 
                request_text_umls:
    """

    def __init__(self):
        pass

    def create_url(self,kind,list_var={}):

        """Dado el tipo de url, crea el link para realizar la peticion.

            Parametros
            ----------
                kind: String
                    Tipo de petición a realizar en la API. Ex: Eutirox

            Retorna
            -------
                url: String
                    Url para realizar la peticion, Ex: https://uts-ws.nlm.nih.gov/rest/search/current?string=dermatitis alérgica&sabs=MDRSPA,SCTSPA,MSHSPA&returnIdType=code&apiKey=<key>&pageNumber=1&searchType=exact

        """

        url = umls_url + kind

        for index, (key, value) in enumerate(list_var.items()):
            if isinstance(value,int):
                url += "&" + key + "=" + str(value)
            elif isinstance(value,str):
                url += "&" + key + "=" + value

        return url

    def request_text_umls(self,text):
        """Devuelve las coincidencias con el texto proporcionado para encontrar reacciones adversas.

            Parametros
            ----------
                text: String
                    Texto a buscar en el tesaurio. Ex: Eutirox

            Retorna
            -------
                text: json
                    Contiene las coincidencias encontradas que coincide con el texto proporcionado.

                resp_code: int
                    Codigo de respuesta de nuestra consulta. Ex: 200
        """

        join_path = "/search/current?"

        dic_var = {
            "string": text,
            "sabs": "MDRSPA,SCTSPA,MSHSPA",
            "returnIdType": "code",
            'pageNumber': 1,
            "searchType": "exact",
            "apiKey":umls_api_key
        }

        url = self.create_url(join_path,dic_var)

        response = requests.get(url,timeout=timeout_value)
        resp_code = response.status_code
        resp_message = response.json()

        return resp_message,resp_code