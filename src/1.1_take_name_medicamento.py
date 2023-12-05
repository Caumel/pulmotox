import sys
import os
sys.path.append('../')
os.chdir('../')
from src import utils

if __name__ == '__main__':
    filename = "data/nombres_2023-11-29 11:20:29.txt"
    medicamentos = utils.get_med_nregistro_name_repeated(filename)
    lista_nombres, new_list_medicamentos = utils.add_name_to_medicamento(medicamentos)
    utils.save_names_per_line_list("data/nombres_no_repetead.txt",new_list_medicamentos)
    utils.save_lista("data/lista_nombre.txt",lista_nombres,'w')