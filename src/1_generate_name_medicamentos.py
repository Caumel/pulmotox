import sys
import os
sys.path.append('../')
os.chdir('../')
import string
from cima import cima_api as cimaAPI
from datetime import datetime
from src.utils import utils

cima = cimaAPI.MyCimaAPI()

path = "data/medicamentos"

def generar_convinaciones():
    letras = string.ascii_uppercase

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"./data/nombres_{now}.txt"

    if os.path.exists(filename):
        os.remove(filename)
        print(f"El archivo {filename} ha sido borrado.")
    else:
        print(f"El archivo {filename} no existe.")

    start = False
    for letra1 in letras:
        for letra2 in letras:
            combinacion = letra1 + letra2
            # if combinacion=="WH":
            #     start = True
            # if start:
            #Tomo todos los medicamentos que tengan la combinacion de letras
            list_elements = cima.get_medicamentos_all(name=combinacion)

            #Tomo listas 
            nombres,objects = utils.get_data(list_elements)

            utils.save_files(path,objects)
            utils.save_names_per_line_list(filename,nombres)

if __name__ == '__main__':
    generar_convinaciones()
