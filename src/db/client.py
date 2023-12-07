"""
Módulo que incluye las funciones de acceso a la base de datos
"""

import json

from pymongo import MongoClient


class DBClient:
    """Cliente de base de datos

    Esta clase incluye los métodos de acceso a la base de datos
    utilizada. Se cubrirán las funcionalidades de
    creación, edición, eliminación de los documentos de cada colección.

    Attributes:
        client (MongoClient): Cliente de la librería pymongo para acceder
        a la base de datos.

    Args:
        url (str): Dirección de la base de datos MongoDB
        database_name (str): Nombre de la base de datos de interacción
        mongo_user (str): Nombre de usuario para la autentificación en
                          la base de datos
        mongo_pass (str): Contraseña del usuario en la base de datos.
        mongo_authdb (str): Nombre de la base de datos de autentificación
    """
    def __init__(self, url, database_name, mongo_user, mongo_pass, 
                 mongo_authdb, port=27017):
        self.client = MongoClient(host=url,
                                  port=port,
                                  username=mongo_user,
                                  password=mongo_pass,
                                  authSource=mongo_authdb)
        self.database = database_name

    def clean_collection(self, collection):
        """
        Borra todos los documentos de la colección indicada

        Args:
            collection (str): Nombre de la colección a la que se
                              eliminarán todos los documentos.

        Returns:
            Boolean: True si la colección ha sido vaciada correctamente
                     False en caso de que la colección no exista.
        """
        self.client[self.database][collection].drop()

    def find_one(self, collection, query, mongoID=False):
        """
        Chequea si existe el documento en nuestra base de datos y
        devuelve una consulta con los datos del documento en caso de
        encontrarlo. Sólamente se busca la primera ocurrencia 'find_one'.

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'find_one'
            query (dict): contiene la query de consulta en la colección.
                          Ejem, {"username": "defensa"}
            mongoID (bool): Evaluación de si queremos obtener el
                            identificador de mongo para cada uno de
                            los elementos encontrados

        Returns:
            diccionario: Diccionario que contiene la información de la
                         consulta para cada búsqueda.
                         Devuelve "None" si la query buscada
                         no existe en nuestra base de datos.
        """
        if mongoID is False:
            result = self.client[self.database][collection].find_one(
                query,
                {"_id": 0}
            )
        elif mongoID is True:
            result = self.client[self.database][collection].find_one(
                query
            )
        else:
            raise ValueError("Expected mongoID as True or False")

        return result

    def find(self, collection, query, mongoID=False):
        """
        Chequea si existes documentos en nuestra base de datos
        que cumplan con las condiciones de query y devuelve una
        consulta con los datos de los documentos en caso de encontrarlos.
        Se buscan todos los documentos que concuerden con la query 'find'.

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'find'
            query (dict): contiene la query de consulta en la colección.
                          Ejem, {"$and": [
                              {'date': {
                                  '$gte': '2020-21-10',
                                  '$lt': '2020-30-11'
                               }},
                               {'cloudCoverage': {
                                   '$lt': 23
                               }}
                            ]}
            mongoID (bool): Evaluación de si queremos obtener el
                            identificador de mongo para cada uno de
                            los elementos encontrados

        Returns:
            list: Lista de productos (cada uno en un diccionario) que cumplen
                   con los requisitos de búsqueda.
        """
        if mongoID is False:
            filtered_products_cursor = self.client[self.database][collection].find(
                                                                query, {"_id": 0})
        elif mongoID is True:
            filtered_products_cursor = self.client[self.database][collection].find(
                                                                query)
        else:
            raise ValueError("Expected mongoID as True or False")

        return list(filtered_products_cursor)
    
    def insert_one(self, collection, new_document):
        """
        Añade un nuevo documento a la colección indicada

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'find_one'
            new_document (dict): contiene el nuevo documento a inserta encontrar
                                 la colección. Ejem, {"username": "defensa"}

        Returns:
            diccionario: Diccionario que contine el resultado de la inserción
                         con el campo 'inserted_id' que indica el ID del
                         nuevo documento insertado.
        """
        result = self.client[self.database][collection].insert_one(new_document)

        return result

    def insert_many(self, collection, new_documents):
        """
        Añade varios documentos a la colección indicada

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'find_one'
            new_documents (list(dict)): contiene el listado con los nuevos
                                        documentos a inserta.
                                        Ejem, [{"username": "defensa"},
                                               {"username": "defensa2"}]

        Returns:
            InsertManyResult: Listado de los _ids de los documentos insertados
        """
        result = self.client[self.database][collection].insert_many(new_documents)

        return result

    def update_one(self, collection, query, update, operator = "set"):
        """
        Actualiza un nuevo documento a la colección indicada

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'find_one'
            query (dict): contiene la query de consulta en la colección.
                          Ejem, {'providerId': _id}
            update (dict): contiene la información a actualizar en la coleccion.
                            Ejem, {'metadata.EPSG': EPSG}

        Returns:
            Instancia de la clase UpdateResult
        """
        result = self.client[self.database][collection].update_one(query, { "$" + operator:update}, upsert=False)

        return result

    def update_many(self, collection, query, update):
        """
        Actualiza varios documentos a la colección indicada.

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'find_one'
            query (dict): contiene la query de consulta en la colección.
                          Ejem, {'providerId': _id}
            update (dict): contiene la información a actualizar en la coleccion.
                            Ejem, {'metadata.EPSG': EPSG}

        Returns:
            Instancia de la clase UpdateResult
        """
        result = self.client[self.database][collection].update_many(query, {"$set":update}, upsert=False)

        return result

    def delete_one(self, collection, query):
        """
        Elimina un documento de la colección indicada.

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectuará el 'delete_one'
            query (dict): contiene la query de consulta en la colección.
                          Ejem, {'providerId': _id}

        Returns:
            Instancia de la clase DeleteResult
        """
        result = self.client[self.database][collection].delete_one(query)

        return result

    def delete_field(self, collection, query, field):
        """
        Elimina un campo determinado de un documento de Pymongo (tanto la
        clave como el valor).

        Args:
            collection (str): Nombre de la colección sobre la que se
                              efectiará el 'delete_field'
            query (dict): Contiene la query de consulta en la colección.
            field (str): Dirección relativa dentro del documento del campo
                         que queremos eliminar.
        
        Returns:
            Instancia de la clase UpdateResult
        """
        result = self.client[self.database][collection].update_one(query,
                                                                   {"$unset": {field: None}},
                                                                   upsert=False)
    
        return result