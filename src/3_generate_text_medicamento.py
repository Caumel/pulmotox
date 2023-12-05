import sys
import os
sys.path.append('../')
os.chdir('../')
import json
import string
import time
from cima import cima_api as cimaAPI
from datetime import datetime
from src import utils

cima = cimaAPI.MyCimaAPI()

def main(filename):
    medicamentos = utils.get_med_nregistro_name(filename)
    for medicamento in medicamentos:
        lista_mal = []
        nregistro = next(iter(medicamento))
        name = medicamento[nregistro]
        text_info, status = cima.get_info_medicamento_section(typeDoc=1,nregister=nregistro,section="")
        if text_info == None:
            lista_mal.append(nregistro)
            utils.save_lista("data/lista_mal_info.txt",lista_mal,"a")
        if status == 200:
            utils.save_json(text_info,f"data/medicamentos_info/{nregistro}.json")
        else:
            print(f"Error al realizar la peticion para el medicamento {nregistro}, con nombre {name}")

if __name__ == '__main__':
    filename = "data/nombres_pactivo_2023-11-30 16:30:30.txt"
    main(filename)
