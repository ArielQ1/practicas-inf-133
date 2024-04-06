import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"

#POST crear un aminal
ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "Gogui",
    "especie": "perro",
    "genero": "macho",
    "edad": 40,
    "peso": 60
}
post_response = requests.post(url=ruta_post, json=nuevo_animal)
print(post_response.text)

#GET listar todos los animales
ruta_get = url + "animales"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#GET animales por especie
ruta_get = url + "animales/?especie=felino"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#GET animales por genero
ruta_get = url + "animales/?genero=macho"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#PUT actualizar la informacion de un animal
ruta_put = url + "animales/2"
animal_actualizado = {
    "nombre": "xxx",
    "especie": "xxx",
    "genero": "xxx",
    "edad": 10,
    "peso": 10
}
put_response = requests.put(url=ruta_put, json=animal_actualizado)
print(put_response.text)

#DELETE eliminar un animal por id
ruta_delete = url + "animales/1"
delete_response = requests.delete(url=ruta_delete)
print(delete_response.text)