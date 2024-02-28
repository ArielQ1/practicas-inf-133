from http.server import HTTPServer, BaseHTTPRequestHandler
import json



estudiantes = [
    {
        "id": 1,
        "nombre": "Ariel",
        "apellido": "Quizaya",
        "carrera-mencion": "Seguridad de la Informacion",
    },
    {
        "id": 2,
        "nombre": "Fabricio",
        "apellido": "Quispe",
        "carrera-mencion": "Seguridad de la Informacion",
    },
    {
        "id": 3,
        "nombre": "Ghilmar",
        "apellido": "Valeirano",
        "carrera-mencion": "Desarrollo de Software",
    },
    {
        "id": 4,
        "nombre": "Pica",
        "apellido": "Valencia",
        "carrera-mencion": "Inteligencia Artificial",
    },
    {
        "id": 5,
        "nombre": "Juan",
        "apellido": "Quispe",
        "carrera-mencion": "Desarrollo de Software",
    },
    {
        "id": 6,
        "nombre": "Pedrito",
        "apellido": "Guzman",
        "carrera-mencion": "TIC",
    },
]

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/lista_estudiantes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(estudiantes).encode('utf-8'))
        elif self.path == '/buscar_nombre':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            nombres_estu = [estudiante['nombre'] for estudiante in estudiantes if estudiante['nombre'].startswith('P')]
            self.wfile.write(json.dumps({"nombres de estudiantes que inician con P": nombres_estu}).encode('utf-8'))
        elif self.path == '/contar_carreras':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()            
            carreras_mencion = [carrera['carrera-mencion'] for carrera in estudiantes]
            carreras_almacendas = {}
            for carrera in carreras_mencion:
                if carrera in carreras_almacendas:
                    carreras_almacendas[carrera] += 1         
                else:
                    carreras_almacendas[carrera] = 1   
            self.wfile.write(json.dumps({"Estudiantes por carrera-mencion": carreras_almacendas}).encode('utf-8'))
        elif self.path == '/total_estudiantes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()        
            self.wfile.write(json.dumps({'El total de Estudiantes es':len(estudiantes)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no existente"}).encode('utf-8'))

def run_server(port = 8000):
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f'Iniciando el servidor web en http://localhost:{port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Apagando Servidor Web')
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
