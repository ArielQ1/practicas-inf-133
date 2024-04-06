import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"

# POST crear un nuevo paciente por la ruta /paciente
ruta_post = url + "pacientes"
nuevo_paciente = {
        "ci": 7147859,
        "nombre": "Pedrito",
        "apellido": "Bustamante",
        "edad": 35,
        "genero": "masculino",
        "diagnostico": "diabetes",
        "doctor": "Pedro Pérez"
}
post_response = requests.post(url=ruta_post, json=nuevo_paciente)
print(post_response.text)

#GET listar todos  los pacientes
ruta_get = url + "pacientes"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#GET buscar Pacientes por ci en proceso
ruta_get = url + "pacientes/6814344"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#GET pacientes con diabetes
ruta_get = url + "pacientes/?diagnostico=diabetes"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#GET pacientes con el doctor Pedro Pérez
ruta_get = url + "pacientes/?doctor=Pedro Pérez"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#PUT Actualizar a un paciente
ruta_put = url + "pacientes/7147859"
update_paciente = {
        "nombre": "Juanito",
        "apellido": "Barrientos",
        "edad": 15,
        "genero": "masculino",
        "diagnostico": "gripe",
        "doctor": "Ghilmar"
}

put_response = requests.put(url=ruta_put, json=update_paciente)
print(put_response.text)

#DELETE eliminar un paciente por ci
ruta_delete = url + "pacientes/6814344"
delete_response = requests.delete(url=ruta_delete)
print(delete_response.text)