from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id": 1,
        "nombre": "Lucy",
        "especie": "felino",
        "genero": "hembra",
        "edad": 5,
        "peso": 15
    },
    {
        "id": 2,
        "nombre": "Nana",
        "especie": "perro",
        "genero": "hembra",
        "edad": 24,
        "peso": 45
    },
    {
        "id": 3,
        "nombre": "Kira",
        "especie": "felino",
        "genero": "hembra",
        "edad": 4,
        "peso": 10
    },
    {
        "id": 3,
        "nombre": "Maxi",
        "especie": "perro",
        "genero": "macho",
        "edad": 36,
        "peso": 55
    },
    
]

class AnimalesService:
    @staticmethod
    def add_animal(data):
        data["id"] = len(animales) + 1
        animales.append(data)
        return animales
    @staticmethod
    def filter_animales_especie(especie):
        return [
            animal for animal in animales if animal["especie"] == especie
        ]
    @staticmethod
    def filter_animales_genero(genero):
        return[
            animal for animal in animales if animal["genero"] == genero
        ]
        
    @staticmethod
    def update_animal(id,data):
        animal = AnimalesService.find_animal(id)
        if animal:
            animal.update(data)
            return animales
        else:
            return None
    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )
        
    @staticmethod
    def delete_animal(id):
        animal = AnimalesService.find_animal(id)
        if animal:
            animales.remove(animal)
            return animales
        else:
            return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
class RESTRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/animales":
            HTTPResponseHandler.handle_response(self, 201, animales)
        elif self.path.startswith("/animales") and "especie" in query_params:
            especie = query_params["especie"][0]
            animales_especie = AnimalesService.filter_animales_especie(especie)
            if animales_especie != []:
                HTTPResponseHandler.handle_response(self, 200, animales_especie)
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        elif self.path.startswith("/animales") and "genero" in query_params:
            genero = query_params["genero"][0]
            animales_genero = AnimalesService.filter_animales_genero(genero)
            if animales_genero != []:
                HTTPResponseHandler.handle_response(self, 200, animales_genero)
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existe"})
        
    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animales = AnimalesService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animales)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animales = AnimalesService.update_animal(id, data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )        
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animales = AnimalesService.delete_animal(id)
            HTTPResponseHandler.handle_response(self, 200, animales)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()