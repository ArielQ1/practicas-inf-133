import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /estudiantes
ruta_get = url + "estudiantes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega 2 estudiantes de Economia
ruta_post = url + "estudiantes"
nuevo_estudiante = {
    "nombre": "Juanito",
    "apellido": "Pérez",
    "carrera": "Economia"
}

post_response = requests.request(method="POST", 
                        url=ruta_post,
                        json=nuevo_estudiante)
print(post_response.text)

nuevo_estudiante = {
    "nombre": "Pedrito",
    "apellido": "Lopez",
    "carrera": "Economia",
}

post_response = requests.request(method="POST", url=ruta_post, json=nuevo_estudiante)
print(post_response.text)

#Consumiendo Ruta Mostrar todas las carreras
ruta_get = url + "carreras/"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#Consumiendo Ruta que devuelva todos los estudiantes de economia
ruta_get = url + "economia/"
get_response = requests.request(method='GET', url=ruta_get)
print(get_response.text)