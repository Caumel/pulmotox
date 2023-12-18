import sys
import os
sys.path.append('../')
os.chdir('../')
from cima import cima_api as cimaAPI
from datetime import datetime
from src.utils import utils

cima = cimaAPI.MyCimaAPI()

def main(filename):
    medicamentos = utils.get_med_nregistro_name(filename)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_pactivo = f"./data/nombres_pactivo_{now}.txt"
    pactivos_lista = []
    for medicamento in medicamentos:
        lista_mal = []
        nregistro = next(iter(medicamento))
        name = medicamento[nregistro]
        # print(nregistro,name)
        text_pactivo, status = cima.get_medicamento(cn="",nregister=nregistro)
        if text_pactivo == None:
            lista_mal.append(nregistro)
            utils.save_lista("data/lista_mal.txt",lista_mal,'a')
        if status == 200:
            pactivos = text_pactivo["pactivos"].split(", ")
            utils.save_lista("data/lista_pactivos.txt",pactivos,'a')
            medicamento["pactivos"] = text_pactivo["pactivos"]
            utils.save_names_per_line(filename_pactivo,medicamento)
            utils.save_json(text_pactivo,f"data/medicamentos_completos/{nregistro}_update.json")
        else:
            print(f"Error al realizar la peticion para el medicamento {nregistro}, con nombre {name}")
   
if __name__ == '__main__':
    filename = "data/nombres_no_repetead.txt"
    main(filename)
