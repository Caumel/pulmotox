import os
import pytest
from src.umls import umls_api as API

umls_api_key = os.getenv('UMLS_API_KEY', '577c8f76-500d-4e94-9139-8a798bdbe78f')

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
    """Funcion para instanciar una api de UMLS

    Retorna:
        MyUmlsAPI: Instancia umls api
    """
    return API.MyUmlsAPI()

def test_create_url(api):
    dic_var = {
        "string": "a",
        "sabs": "MDRSPA,SCTSPA,MSHSPA",
        "returnIdType": "code",
        'pageNumber': 1,
        "searchType": "exact",
        "apiKey":umls_api_key
    }
    join_path = "/search/current?"
    url_method = api.create_url(join_path,dic_var)
    url = "https://uts-ws.nlm.nih.gov/rest/search/current?&string=a&sabs=MDRSPA,SCTSPA,MSHSPA&returnIdType=code&pageNumber=1&searchType=exact&apiKey=577c8f76-500d-4e94-9139-8a798bdbe78f"
    assert url_method == url

def test_request_text_umls(api):
    text = "cabeza"
    response, code = api.request_text_umls(text)
    test_text = [{'ui': '69536005', 'rootSource': 'SCTSPA', 'uri': 'https://uts-ws.nlm.nih.gov/rest/content/2023AB/source/SCTSPA/69536005', 'name': 'estructura de la cabeza'}, {'ui': 'D006257', 'rootSource': 'MSHSPA', 'uri': 'https://uts-ws.nlm.nih.gov/rest/content/2023AB/source/MSHSPA/D006257', 'name': 'Cabeza'}]
    assert code == 200 \
            and all(elem in response["result"]["results"] for elem in test_text) 

