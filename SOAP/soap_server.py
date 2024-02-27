from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler


def sumaNumeros(num1, num2):
    return "La suma de los numeros {} y {} es : {} ".format(num1,num2,int(num1)+int(num2))

dispatcher = SoapDispatcher(
    "suma-de-numeros",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace = True,
    ns = True,
)

dispatcher.register_function(
    "SumaDosNumeros",
    sumaNumeros,
    returns={"SumaDosNumeros": str},
    args={"num1": int, "num2": int}
)

server = HTTPServer(("0.0.0.0", 8000),SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()