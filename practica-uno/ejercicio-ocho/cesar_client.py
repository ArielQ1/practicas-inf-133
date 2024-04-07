import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"

#POST crear un mensaje
ruta_post = url + "mensajes"
nuevo_mensaje = {
    "contenido": "Hola mundo"
}
post_response = requests.post(url=ruta_post, json=nuevo_mensaje)
print(post_response.text)
ruta_post = url + "mensajes"
nuevo_mensaje = {
    "contenido": "aprendiendo a encriptar por el cesar"
}
post_response = requests.post(url=ruta_post, json=nuevo_mensaje)
print(post_response.text)

#GET listar todos los mensajes
ruta_get = url + "mensajes"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#GET buscar mensajes por id
ruta_get = url + "mensajes/1"
get_response = requests.get(url=ruta_get)
print(get_response.text)

#PUT actualizar un mensaje
ruta_put = url + "mensajes/1"
update_mensaje = {
    "contenido": "david perro"
}
put_response = requests.put(url=ruta_put, json=update_mensaje)
print(put_response.text)

#DELETE eliminar un mensajes
ruta_delete = url + "mensajes/1"
delete_response = requests.delete(url=ruta_delete)
print(delete_response.text)