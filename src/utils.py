from bs4 import BeautifulSoup
import requests
import os
import json
import datetime
import json
import re

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