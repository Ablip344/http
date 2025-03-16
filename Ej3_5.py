import requests

url='https://www.zaragoza.es/sede/servicio/urbanismo-infraestructuras/equipamiento/aparcamiento-bicicleta.json?=&rows=1'

response = requests.get(url)

data = response.json()

print(data.keys())