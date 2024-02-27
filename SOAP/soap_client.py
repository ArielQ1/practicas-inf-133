from zeep import Client

client = Client('http://localhost:8000')

result = client.service.SumaDosNumeros(num1=12,num2=17)
print(result)
