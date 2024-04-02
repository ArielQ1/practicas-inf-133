from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def suma (a, b):
    return "!El Resultado de la suma es: {}!".format(a+b)
def resta (a, b):
    return "!El Resultado de la resta es: {}!".format(a-b)
def multiplicacion (a, b):
    return "!El Resultado de la multiplicaion es: {}!".format(a*b)
def divicion (a, b):
    return "!El Resultado de la divicion es: {}!".format(a/b)


dispatcher = SoapDispatcher(
    "soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace = True,
    ns = True,    
)

dispatcher.register_function(
    "Suma",
    suma,
    returns={"suma": str},
    args={"a": int, "b":int},
)
dispatcher.register_function(
    "Resta",
    resta,
    returns={"resta": str},
    args={"a": int, "b":int},
)
dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"multiplicacion": str},
    args={"a": int, "b":int},
)
dispatcher.register_function(
    "Divicion",
    divicion,
    returns={"divicion": str},
    args={"a": int, "b":int},
)

server = HTTPServer(("0.0.0.0", 8000),SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()