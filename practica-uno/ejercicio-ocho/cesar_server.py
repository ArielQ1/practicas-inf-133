from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

mensajes = [
    {
        "id":1,
        "contenido":"hola",
        "contenido_encriptado": "krod"
    }
]

class MensajeService:
    @staticmethod
    def add_mensaje(data):
        data["contenido_encriptado"] = MensajeService.encriptado_cesar(data["contenido"])
        data["id"] = len(mensajes)+1 
        mensajes.append(data)
        return mensajes

    @staticmethod
    def encriptado_cesar(text):
        mensaje_encriptado = ""
        for i in range(len(text)):
             letra = ord(text[i])+3
             mensaje_encriptado += chr(letra)
        return mensaje_encriptado
    
    @staticmethod
    def find_mensaje(id):
        return next(
            (mensaje for mensaje in mensajes if mensaje["id"] == id),
            None,
        )
        
    @staticmethod
    def update_mensaje(id, data):
        mensaje = MensajeService.find_mensaje(id)
        data["contenido_encriptado"] = MensajeService.encriptado_cesar(data["contenido"]) 
        if mensaje:
            mensaje.update(data)
            return mensajes
        else:
            return None
    
    @staticmethod
    def delete_mensaje(id):
        mensaje = MensajeService.find_mensaje(id)
        if mensaje:
            mensajes.remove(mensaje)
            return mensajes
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
        if parsed_path.path == "/mensajes":
            HTTPResponseHandler.handle_response(self, 201, mensajes)
        
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            paciente = MensajeService.find_mensaje(id)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])    
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
            
    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            pacientes = MensajeService.add_mensaje(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            mensajes = MensajeService.update_mensaje(id, data)
            if mensajes:
                HTTPResponseHandler.handle_response(self, 200, mensajes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Estudiante no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensajes = MensajeService.delete_mensaje(id)
            HTTPResponseHandler.handle_response(self, 200, mensajes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
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
