from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


animales = {}

class ZooAminal:
    def __init__(self, animal_type, id, especie, genero, edad, peso):
        self.animal_type = animal_type
        self.id = id
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class Mamifero (ZooAminal):
    def __init__(self, id, especie, genero, edad, peso):
        super().__init__("mamifero", id, especie, genero, edad, peso)

class Ave (ZooAminal):
    def __init__(self, id, especie, genero, edad, peso):
        super().__init__("ave", id, especie, genero, edad, peso)

class Reptil (ZooAminal):
    def __init__(self, id, especie, genero, edad, peso):
        super().__init__("reptil", id, especie, genero, edad, peso)

class Anfibio (ZooAminal):
    def __init__(self, id, especie, genero, edad, peso):
        super().__init__("anfibio", id, especie, genero, edad, peso)

class Pez (ZooAminal):
    def __init__(self, id, especie, genero, edad, peso):
        super().__init__("pez", id, especie, genero, edad, peso)
        
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type, id, especie, genero, edad, peso):
        if animal_type == "mamifero":
            return Mamifero(id, especie, genero, edad, peso)
        elif animal_type == "ave":
            return Ave(id, especie, genero, edad, peso)
        elif animal_type == "reptil":
            return Reptil(id, especie, genero, edad, peso)
        elif animal_type == "anfibio":
            return Anfibio(id, especie, genero, edad, peso)
        elif animal_type == "pez":
            return Pez(id, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no valido")
        
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))
    
class ZooService:
    def __init__(self):
        self.factory = AnimalFactory()
        
    def add_animal(self, data):
        animal_type = data.get("animal_type", None)
        id = data.get("id", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)
        
        factory_animal = self.factory.create_animal(animal_type, id,especie, genero, edad, peso)
        
        if animales:  
            max_key = max(animales.keys())  
            new_key = max_key + 1 
        else:
            new_key = 1

        animales[new_key] = factory_animal
        
        return factory_animal
    
    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    
    def animales_especies(self, especie):
        return {index : animal.__dict__ for index, animal in animales.items() if animal.especie == especie}
    
    def animales_genero(self, genero):
        return {index : animal.__dict__ for index, animal in animales.items() if animal.genero == genero}
    
    def update_animal(self, animal_id, data):
        if animal_id not in animales:
            return None
        
        animal = animales[animal_id]
        animal.especie = data.get("especie", animal.especie)
        animal.genero = data.get("genero", animal.genero)
        animal.edad = data.get("edad", animal.edad)
        animal.peso = data.get("peso", animal.peso)
        
        return animal
    
    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"messege": "Animal eliminado"}
        else:
            None
    
class ZooRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoo_service = ZooService()
        super().__init__(*args, **kwargs)
        
    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoo_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
            
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        if self.path == "/animales":
            response_data = self.zoo_service.list_animales()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/animales") and "especie" in query_params:
            especie = query_params["especie"][0]
            animales_especie = self.zoo_service.animales_especies(especie)                
            if animales_especie:
                HTTPDataHandler.handle_response(self, 200, animales_especie)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        elif self.path.startswith("/animales") and "genero" in query_params:
            genero = query_params["genero"][0]
            animales_genero = self.zoo_service.animales_genero(genero)
            if animales_genero:
                HTTPDataHandler.handle_response(self, 200, animales_genero)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
        
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoo_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
            
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoo_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
            
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZooRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
