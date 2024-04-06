from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Mutation, Field

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()
    
plantas = [
    Planta(id=1, nombre="margarita", especie="flor", edad=3, altura=10, frutos=False),
    Planta(id=2, nombre="sandia", especie="tuberculo", edad=7, altura=20, frutos=True),
    Planta(id=3, nombre="girasol", especie="flor", edad=5, altura=35, frutos=False),   
    Planta(id=4, nombre="Naranja", especie="arbol", edad=8, altura=100, frutos=True),   
]

class Query(ObjectType):
    plantas = List(Planta)
    especies = List(Planta, especie=String())
    frutos = List(Planta, frutos=Boolean()) 
    
    def resolve_plantas(root, info):
        return plantas

    def resolve_especies(root, info, especie):
        plantas_de_especie = list(planta for planta in plantas if planta.especie == especie)
        return plantas_de_especie

    def resolve_frutos(root, info, frutos):
        plantas_frutos = list(planta for planta in plantas if planta.frutos == frutos)
        return plantas_frutos
    
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
        
    planta = Field(Planta)
    
    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id = len(plantas) + 1,
            nombre = nombre,
            especie = especie,
            edad = edad,
            altura = altura,
            frutos = frutos   
        )
        plantas.append(nueva_planta)

        return CrearPlanta(planta = nueva_planta)
    
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None
    
class UpdatePlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    
    planta = Field(Planta)
    
    def mutate(root, info,id, nombre, especie, edad, altura, frutos):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                planta.nombre = nombre
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.frutos = frutos
                return UpdatePlanta(planta=planta)
        return None
        
        
class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    update_planta = UpdatePlanta.Field()

schema = Schema(query=Query, mutation=Mutations)
    
class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def do_GET(self):
        if self.path == "/graphql":            
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})    
        
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})
            
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()