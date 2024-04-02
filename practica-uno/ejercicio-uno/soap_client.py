from zeep import Client

client = Client('http://localhost:8000')

result = client.service.Suma(a = 15,b = 25)
print(result)
result = client.service.Resta(a = 15,b = 25)
print(result)
result = client.service.Multiplicacion(a = 15,b = 25)
print(result)
result = client.service.Divicion(a = 15,b = 25)
print(result)
