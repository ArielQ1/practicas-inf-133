import requests

url = "http://localhost:8000/animales"
headers = {'Content-type': 'application/json'}


#POST crear un animal
new_animal = {
    "animal_type": "mamifero",
    "id": 1,
    "especie":"leon",
    "genero":"macho",
    "edad":15,
    "peso":100
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.json())
new_animal = {
    "animal_type": "ave",
    "id": 2,
    "especie":"gorion",
    "genero":"hembra",
    "edad":5,
    "peso":10
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.json())
new_animal = {
    "animal_type": "reptil",
    "id": 3,
    "especie":"lagarto",
    "genero":"macho",
    "edad":15,
    "peso":50
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.json())

#GET listar todos los animales
response = requests.get(url=url)
print(response.json())

#GET buscar animales por especie
response = requests.get(url=url+"/?especie=leon")
print(response.json())

#GET buscar animales por genero
response = requests.get(url=url+"/?genero=macho")
print(response.json())

#PUT actualizar la informacion de un animal
updated_animal = {
    "genero": "hembra"
}
response = requests.put(url=url+"/3", json=updated_animal)
print("Animal actualizado:", response.json())

#DELETE eliminar un animal
response = requests.delete(url=url+"/1")
print("Animal eliminado:", response.json())
