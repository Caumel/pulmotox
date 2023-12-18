import pytest
from src.cima import cima_api as API

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
    """Funcion para instanciar una api de CIMA

    Retorna:
        MyCimaAPI: Instancia cima api
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

    assert code == 200 \
            and reponse["totalFilas"] == 11 \
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
    text, resp_code = api.get_medicamento(nregister=64014)

    assert resp_code == 200 \
            and text["nregistro"] == "64014" \
            and text["nombre"] == "EUTIROX 100 microgramos COMPRIMIDOS" \
            and text["pactivos"] == "LEVOTIROXINA SODICA" \

def test_get_info_medicamento_section_4_8(api):
    text, resp_code = api.get_info_medicamento_section(nregister=64014,section="4.8")

    assert resp_code == 200 \
        and text[0]["seccion"] == "4.8" \
        and text[0]["titulo"] == 'Reacciones adversas' \
        and text[0]["contenido"][:5] == '<div>' \

def test_get_info_medicamento_section(api):
    text, resp_code = api.get_info_medicamento_section(nregister=64014)

    assert resp_code == 200 \
        and text[0]["seccion"] == "1" \
        and text[0]["titulo"] == "NOMBRE DEL MEDICAMENTO" \
        and text[17]["seccion"] == "4.8" \
        and text[17]["titulo"] == 'Reacciones adversas' \
        and text[17]["contenido"][:5] == '<div>' \

def test_get_info_secciones(api):
    text, resp_code = api.get_info_secciones(nregister=64014)
    assert resp_code == 200 \
        and text[0]["seccion"] == "1" \
        and text[0]["titulo"] == "NOMBRE DEL MEDICAMENTO" \
        and text[0]["orden"] == 1 \
        and "contenido" not in text[0] \
        and text[17]["seccion"] == "4.8" \
        and text[17]["titulo"] == 'Reacciones adversas' \
        and text[17]["orden"] == 16 \
        and "contenido" not in text[17] \

def test_buscarEnFichaTecnica(api):
    body = [{
        "seccion":"4.1",
        "texto":"cáncer",
        "contiene":1
    }]
    lista = api.buscarEnFichaTecnica(body)
    medicamentos = {
        'nregistro': '71857', 'nombre': 'ANASTROZOL SANDOZ 1 MG COMPRIMIDOS RECUBIERTOS CON PELÍCULA EFG',
        'labtitular': 'Sandoz Farmaceutica S.A.', 'cpresc': 'Medicamento Sujeto A Prescripción Médica', 
        'estado': {'aut': 1302645600000}, 'comerc': True, 'receta': True, 'generico': True, 'conduc': False, 
        'triangulo': False, 'huerfano': False, 'biosimilar': False, 'nosustituible': {'id': 0, 'nombre': 'N/A'}, 
        'psum': False, 'notas': False, 'materialesInf': False, 'ema': False, 'docs': [{'tipo': 1, 
        'url': 'https://cima.aemps.es/cima/pdfs/ft/71857/FT_71857.pdf', 'urlHtml': 
        'https://cima.aemps.es/cima/dochtml/ft/71857/FT_71857.html', 'secc': True, 'fecha': 1624398171000}, 
        {'tipo': 2, 'url': 'https://cima.aemps.es/cima/pdfs/p/71857/P_71857.pdf', 'urlHtml': 
        'https://cima.aemps.es/cima/dochtml/p/71857/P_71857.html', 'secc': True, 'fecha': 1624398183000}], 
        'fotos': [{'tipo': 'materialas', 'url': 'https://cima.aemps.es/cima/fotos/thumbnails/materialas/71857/71857_materialas.jpg', 
        'fecha': 1529504834000}, {'tipo': 'formafarmac', 
        'url': 'https://cima.aemps.es/cima/fotos/thumbnails/formafarmac/71857/71857_formafarmac.jpg', 'fecha': 1529504836000}], 
        'viasAdministracion': [{'id': 48, 'nombre': 'VÍA ORAL'}], 'formaFarmaceutica': {'id': 42, 
        'nombre': 'COMPRIMIDO RECUBIERTO CON PELÍCULA'}, 'formaFarmaceuticaSimplificada': {'id': 10, 
        'nombre': 'COMPRIMIDO'}, 'vtm': {'id': 108774000, 'nombre': 'anastrozol'}, 'dosis': '1 MG'
    }

    assert len(lista) == 75 \
           and medicamentos in lista

def test_registroCambios(api):
    results = api.registroCambios("18/12/2023")
    lista_elementos = [{'nregistro': '61790', 'fecha': 1702865175000, 'tipoCambio': 2, 'cambio': []}, 
    {'nregistro': '65480', 'fecha': 1702865175000, 'tipoCambio': 2, 'cambio': []}, 
    {'nregistro': '66171', 'fecha': 1702865175000, 'tipoCambio': 2, 'cambio': []}, 
    {'nregistro': '66172', 'fecha': 1702865175000, 'tipoCambio': 2, 'cambio': []}, 
    {'nregistro': '66173', 'fecha': 1702865175000, 'tipoCambio': 2, 'cambio': []}, 
    {'nregistro': '72742', 'fecha': 1702865175000, 'tipoCambio': 2, 'cambio': []}]
    assert all(elem in results for elem in lista_elementos)