# Pulmotox

## Casos de Uso

1: Consulta del Medicamento 

Descripcion:

El médico introduce un medicamento o varios y obtiene la información de lasreacciones adversas (TODAS) se muestras por orden de gravedad y por su actuación sobre diferente aparatos(respiratorio/ circulatorio)
La representación puede realizarse sobre una figura humana indicando con colores al pinchar se expande la información

- Precondición: El medicamento debe estar actualizado
- Postcondición: Se obtiene la información sobre el medicamento / pp activo


2: Caso de Uso	Actualización del Medicamento

Descripcion:

Este caso de uso es solo necesario para mantenier una lista de medicamentos o principios activos o porque almacenamos toda la info en nuestros sistemas

- Precondición: El medicamento debe existir. Entendemos que usamos API y por tanto el medicamento existe. Este caso de uso es solo necesario para mantenier una lista de medicamentos o principios activos o porque almacenamos toda la info en nuestros sistemas
- Postcondición: Se obtiene la información sobre el medicamento / pp activo

## Etapas del proyecto

### ETAPA I

1.	Estudio Funcional
2.	Análisis de Fuentes de Datos
3.	Extracción de la información de todos los medicamentos.
4.	Tratamiento de la sección 4.8 para determinar las reacciones adversas de cada medicamento

### ETAPA II

1.	Creación de BBDD tipo grafo/relacional (a estudiar) para el almacenamiento de la información en modo grafo teniendo en cuenta las siguientes relaciones:
a.	Ser principio de
b.	Ser reacción adversa medicamento
c.	Ser reacción adversa principio

### ETAPA III

1.	Creación de Dashboard para la explotación de la información y poder usar la aplicación para determinar a partir de un conjunto de medicamentos las reacciones adversas asociadas al uso de todos ellos.
2.	Aplicación react para moviles

## Archivos y estructura de carpetas

- .devcontainer
    - devcontainer.json
    - docker-compose.yml
    - Dockerfile
- data
    - medicamentos: Informacion de medicamentos, sin info de pactivo
    - medicamentos_completos: Informacion de medicamento, con info de pactivo
    - medicamentos_info: Informacion en texto de los medicamentos.
    - nombres: todos los nombres de todos los medicamentos, sin info de principio activo
    - nombres_pactivo: todos los nombres de todos los medicamentos, con info de principio activo
- docker
    - docker-compose.yml
    - Dockerfile
- notebooks
    - draft.ipynb: notebooks exploratorio con experimentos de la api
- src
    - cima: metodos para la api
    - db:
    - postprocess:
    - preprocess:
    - web:
    - umls:
    - utils:
- tests
    - data
    - unitary
        -  Cima
- .gitignore
- main.py
- README.md
- requierements.txt

## API

### CIMA

- create_url
- get_medicamentos
- get_medicamentos_all 
- get_medicamento
- get_info_medicamento_section
- get_info_secciones
- buscarEnFichaTecnica
- registroCambios

### UMLS

- create_url
- request_text_umls

## BBDD

### Estructura

## Docker

## Lanzar servicio de pulmotox

Lanzará un contenedor con el servicio de pulmotox e incluirá los datos de configuración.

```python
cd docker
docker-compose up -d
```

## Datos de configuración servicio

Apis:

 - url api cima: https://cima.aemps.es/cima/rest/
 - timeout: 10.

Base de datos:

 - Usuario base de datos: pulmotox
 - Contraseña base de datos: pulmotox-dev
 - Auth source base de datos: pulmotox
 - Puerto base de datos: 27017 

## Tareas que faltan por realizar.

- [X] Crear clase con la API
- [X] Crear docker proyecto despliegue
- [X] Crear docker proyecto develop
- [X] Descargar todos los datos para realizar pruebas
- [X] Descargar pactivos de los datos descargados
- [X] Descargar toda la info de cada medicamento
- [X] Realizar pruebas con la API
- [ ] Metodos para actualizar cada X tiempo los medicamentos que se han actualizado, con registroCambios
- [ ] Automatizar la descarga de los medicamentos y descargar pactivos e info
- [X] Crear web simple con buscador
- [X] Mirar que metodo buscar para sugerir.
- [X] Crear sugerencia de texto al medicamento buscado
- [ ] Mirar que BBDD usar
- [ ] Crear BBDD a usar con los medicamento.
- [ ] Crear metodo para gestions de BBDD
- [...] Base de datos grafos, neo4j
- [X] Test cima
- [ ] Test utils_clean_text
- [...] Test utils
- [X] Test umls

## Error encontrados

- Cuando se hace peticion de medicamentos con TI, da error en algunas paginas, mirar por que.
- Tambien error en TO, en la pagina 20
- No es Error como tal, pero no siempre en la lista de devuelta en forma de json, la posicion 14 corresponde a la seccion 4.8 

https://cima.aemps.es/cima/dochtml/ft/51347/FT_51347.html
https://arrows.app/#/local/id=IZg5noFI2dbeKsggpsSw