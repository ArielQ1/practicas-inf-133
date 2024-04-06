from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": 6814344,
        "nombre": "Pedrito",
        "apellido": "García",
        "edad": 21,
        "genero": "masculino",
        "diagnostico": "diabetes",
        "doctor": "Pedro Pérez"
    },
    {
        "ci": 147859,
        "nombre": "Ana",
        "apellido": "Garcia",
        "edad": 18,
        "genero": "femenino",
        "diagnostico": "gripe",
        "doctor": "Fabricio"
    },

]


class PacientesService:
    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return pacientes
    
    @staticmethod
    def find_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]
        
    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [
            paciente for paciente in pacientes if paciente["doctor"] == doctor
        ]

    @staticmethod
    def update_paciente(ci, data):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None


    @staticmethod
    def delete_paciente(ci):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return pacientes
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
        if parsed_path.path == "/pacientes":
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        elif self.path.startswith("/pacientes") and "diagnostico" in query_params:
            
            diagnostico = query_params["diagnostico"][0]
            pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(
                diagnostico
            )
            if pacientes_filtrados != []:
                HTTPResponseHandler.handle_response(
                    self, 200, pacientes_filtrados
                )
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        elif self.path.startswith("/pacientes") and "doctor" in query_params:
            
            doctor = query_params["doctor"][0]
            pacientes_filtrados = PacientesService.filter_pacientes_by_doctor(
                doctor
            )
            if pacientes_filtrados != []:
                HTTPResponseHandler.handle_response(
                    self, 200, pacientes_filtrados
                )
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
             
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.find_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])            
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
        
        
    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Estudiante no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            # Eliminar un paciente
            ci = int(self.path.split("/")[-1])
            pacientes = PacientesService.delete_paciente(ci)
            HTTPResponseHandler.handle_response(self, 200, pacientes)
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