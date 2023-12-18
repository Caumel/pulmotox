from bs4 import BeautifulSoup
import requests
import os
import json
import datetime
import json
import re
import Levenshtein as lev
from fuzzywuzzy import process
from tqdm import tqdm

import spacy
import re

nlp = spacy.load('es_core_news_sm')

def unit_datetime(unix_date):
    """
    Converts Unix timestamp in milliseconds to a human-readable date-time format in UTC.

    Input:
        unix_date (int): Unix timestamp in milliseconds.

    Output:
        str: Formatted date-time string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    unix_timestamp_in_seconds = unix_date / 1000
    date_time = datetime.datetime.utcfromtimestamp(unix_timestamp_in_seconds)
    formatted_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date
    # unix_timestamp = 1394517843000
    # unit_datetime(unix_timestamp)

def extract_and_clean_text(html_content):
    """
    Parses HTML content and extracts clean text from it.

    Input:
        html_content (str): HTML content to be parsed.

    Output:
        str: Cleaned text extracted from the HTML content.
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text and filter out empty lines
    text = soup.get_text(separator='\n').strip()    
    # Join the lines back into a single string
    return text

def get_med_nregistro_name_repeated(filename):
    """
    Reads a file and extracts unique medicine data based on 'id_medicamento'.

    Input:
        filename (str): Path to the file containing medicine data.

    Output:
        list: List of unique medicines data.
    """
    seen = set()  # Set to store unique medicine names
    unique_meds = []

    with open(filename, "r") as file:
        for line in file:
            data = json.loads(line.strip())
            # med_name = list(data.values())[0]  # Extract the medicine name
            id_medicamento = next(iter(data.keys()))  # Extract the medicine name

            if id_medicamento not in seen:
                seen.add(id_medicamento)  # Add to the set if not seen before
                unique_meds.append(data)  # Add to the list of unique medicines
    return unique_meds

def extract_text_before_number(s):
    """
    Extracts and returns text from a string before the first occurrence of a number.

    Input:
        s (str): The string from which text is extracted.

    Output:
        str: The extracted text or the original string if no number is found.
    """
    expresion = r'^(.*?)(?=\s\d)'
    match = re.search(expresion, s)
    if match:
        return match.group(1)
    else:
        return s  # or return None if you prefer
    
def add_name_to_medicamento(lista_medicamentos):
    """
    Processes a list of medicine data, extracting and adding a 'name' field to each medicine.

    Input:
        lista_medicamentos (list): List of dictionaries, each representing a medicine.

    Output:
        tuple: A tuple containing two lists, one of unique names and the other of updated medicine data.
    """
    new_list_medicamentos = []
    lista_nombres = set()
    for medicamento in lista_medicamentos:
        name = list(medicamento.values())[0]
        result = extract_text_before_number(name)
        medicamento["name"] = result
        lista_nombres.add(result)
        new_list_medicamentos.append(medicamento)
    lista_nombres = list(lista_nombres)
    return lista_nombres, new_list_medicamentos

def save_names_per_line_list(name,lista):
    """
    Appends a list of dictionaries to a file in JSON format, each on a new line.

    Input:
        name (str): Filename to which the data will be appended.
        lista (list): List of dictionaries to be saved.

    Output:
        None: Writes to a file but does not return any value.
    """
    with open(name, 'a') as file:
        for item in lista:
            # Convert the dictionary to a JSON string and write it to the file
            file.write(json.dumps(item) + '\n')

def save_names_per_line(name,medicamento):
    """
    Appends a single dictionary to a file in JSON format.

    Input:
        name (str): Filename to which the data will be appended.
        medicamento (dict): Dictionary to be saved.

    Output:
        None: Writes to a file but does not return any value.
    """
    with open(name, 'a') as file:
        # Convert the dictionary to a JSON string and write it to the file
        file.write(json.dumps(medicamento) + '\n')

def read_names_medicamentos(path):
    """
    Reads a txt with all the names of all the medicaments

    Input:
        path (String): path of the file

    Output:
        names (List): list of names of medicaments
    """
    with open(path, 'r') as file:
        content = file.read()
    # Split the content by ':' and remove any whitespace
    names = [num.strip() for num in content.split(':')]
    return names

def get_med_nregistro_name(filename):
    """
    Reads a JSON formatted file and returns a list of dictionaries.

    Input:
        filename (str): Path to the file to be read.

    Output:
        list: List of dictionaries read from the file.
    """
    with open(filename,"r") as file:
        # Read lines into a list
        lines = [json.loads(line.strip()) for line in file]
    return lines

def save_json(text,filename):
    """
    Saves a given data structure in JSON format to a specified file.

    Input:
        text (any serializable data): Data to be saved in JSON format.
        filename (str): Path to the file where data will be saved.

    Output:
        None: Writes to a file but does not return any value.
    """
    with open(filename, 'w') as file:
        json.dump(text, file, indent=4)

def save_lista(name, lista, _type="a"):
    """
    Writes a list of elements to a file, separating them with colons.

    Input:
        name (str): Path to the file where data will be saved.
        lista (list): List of elements to be written to the file.
        _type (str): Write mode for the file ('a' for append, 'w' for write).

    Output:
        None: Writes to a file but does not return any value.
    """
    with open(name, _type) as archivo:
        for elemento in lista:
            archivo.write(elemento + ':')

def save_files(path,lista):
    """
    Saves each item in a list of dictionaries to a separate file, named using a key from the dictionary.

    Input:
        path (str): Directory path where files will be saved.
        lista (list): List of dictionaries to be saved.

    Output:
        None: Writes to files but does not return any value.
        Side effect: Prints a message if a file already exists.
    """
    for index, item in enumerate(lista):
        # Create a unique file name for each dictionary
        file_name = os.path.join(path,f"{item['nregistro']}.txt")
        if os.path.exists(file_name):
            print(f"El archivo {file_name} ya existe")
        else:
            with open(file_name, 'w') as file:
                # Convert the dictionary to a JSON string and write it to the file
                file.write(json.dumps(item))

def get_data(list_elements_to_get_names):
    """
    Extracts specific data from each element of a list of dictionaries.

    Input:
        list_elements_to_get_names (list): List of dictionaries from which data is extracted.

    Output:
        tuple: A tuple containing two lists, one with specific data extracted and the other with the original elements.
    """
    list_names = []
    list_objects = []
    for element in list_elements_to_get_names:
        list_names.append({element["nregistro"]:element["nombre"]})#.split(" ")[0])
        list_objects.append(element)#.split(" ")[0])
    return list_names,list_objects





# Function to suggest words
def suggest_word(input_word, database, max_distance=3):
    suggestions = []
    for word in database:
        if lev.distance(input_word.lower(), word.lower()) <= max_distance:
            suggestions.append(word)
    return suggestions

def get_similar_words(query, word_list, limit=5):
    """
    Find similar words in a list to the given query word.
    
    :param query: The word to match.
    :param word_list: A list of words to search in.
    :param limit: Number of top matches to return. Defaults to 5.
    :return: List of tuples with matching word and similarity score.
    """
    # Use the process.extract function to find similar words
    similar_words = process.extract(query, word_list, limit=limit)
    return similar_words


##############################
#                            #
#        Clean text          #
#                            #
##############################

def read_medicamento_info(filename):
    with open(filename,"r") as file:
        data = json.load(file)
    return data

# Función para limpiar el texto
def limpiar_texto(texto):
    # Eliminar caracteres especiales y números
    texto = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', texto)
    # Convertir a minúsculas
    return texto.lower()

# Lematizar el texto
def lematizar_texto(texto):
    doc = nlp(texto)
    return ' '.join([token.lemma_ for token in doc])


##############################
#                            #
#            UMLS            #
#                            #
##############################

def get_pairs(lists):
    pairs = []
    for lst in lists:
        for i in range(len(lst) - 1):
            pairs.append((lst[i], lst[i+1]))
    return pairs

def remove_duplicated(lista):
    return list(set(map(str.lower, lista)))

def seach_for_p_activo(lista,nregistro):
    # Busco los pactivos
    for linea in lista:
        if next(iter(linea)) == nregistro:
            p_activo = linea["pactivos"]
    return p_activo

def search_reacciones_adversas(texto_analizar,umls):
    pairs = get_pairs(texto_analizar)
    reacciones_adversas = []
    for pair in tqdm(pairs):
        text = pair[0] + " " + pair[1]
        response, code = umls.request_text_umls(text)
        if response["result"]["results"] is not None:
            for index,element in enumerate(response["result"]["results"]):
                reacciones_adversas.append(element["name"])
        else:
            continue
    return remove_duplicated(reacciones_adversas)

