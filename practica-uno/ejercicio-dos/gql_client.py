import requests

# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

#Definir Consulta Crear Planta
query_crear = '''
    mutation {
        crearPlanta(nombre: "Amapola", especie: "flor", edad: 5, altura: 10, frutos: false) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
'''

# Consulta Crear
response = requests.post(url, json={'query':query_crear})
print(response.text)

# Definir la consulta Listar Plantas
query_plantas = '''
    {
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
'''
#Consulta Listar Pantas
response = requests.get(url, json={'query': query_plantas})
print(response.text)

#Definir la consulta buscar plantas por especie
query_especies = '''
    {
        especies(especie:"flor"){
            id
            nombre
            especie
        }
    }
'''
#Consulta especies
response = requests.get(url, json={'query': query_especies})
print(response.text)

#Definir la consulta para las plantas con frutos
query_frutos = '''
    {
        frutos(frutos:true){
            id
            nombre
            frutos
        }
    }
'''
#Consulta Frutos
response = requests.get(url, json={'query':query_frutos})
print(response.text)

#Actualizar la Informacion de una Planta
query_actualizar = '''
    mutation {
        updatePlanta(id: 2, nombre: "Gladiolo", especie: "flor", edad: 8, altura: 20, frutos: false){
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
'''

#Consulta Actualizar
response = requests.post(url, json={'query': query_actualizar})
print(response.text)

#Definir Consulta Eliminar Planta
query_eliminar = '''
    mutation {
        deletePlanta(id: 5) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
'''
# Consulta Eliminar
response = requests.post(url, json={'query': query_eliminar})
print(response.text)
