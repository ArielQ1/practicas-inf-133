import requests
url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}


#POST crear un paciente
paciente = {
    "ci": 7147859,
    "nombre": "Pedrito",
    "apellido": "Bustamante",
    "edad": 35,
    "genero": "masculino",
    "diagnostico": "diabetes",
    "doctor": "Ghilmar"
}
response = requests.post(url, json=paciente, headers=headers)
print(response.json())
#POST crear un paciente
paciente = {
    "ci": 6814344,
    "nombre": "Pedrito",
    "apellido": "García",
    "edad": 21,
    "genero": "masculino",
    "diagnostico": "diabetes",
    "doctor": "Pedro Pérez"
}
response = requests.post(url, json=paciente, headers=headers)
print(response.json())

#GET listar todos los pacientes
response = requests.get(url)
print(response.json())

#GET pacientes ci
response = requests.get(url+"/6814344")
print(response.json())

#GET Listar a los pacientes que tienen diagnostico de Diabetes
response = requests.get(url+"/?diagnostico=diabetes")
print(response.json())

#GET listar a los pacientes que atiende el doctor Pedro Pérez
response = requests.get(url+"/?doctor=Pedro Pérez")
print(response.json())

#UPDATE actualizar la informacion de un paciente
actualizacion_paciente = {
    "edad": 21,
    "doctor": "Doctor Pedro Perez",
}
response = requests.put(url+"/7147859", json=actualizacion_paciente)
print(response.json())

#DELETE eliminar un paciente
response = requests.delete(url + "/1")
print(response.json())

