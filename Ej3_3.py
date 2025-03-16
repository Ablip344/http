import requests

url='https://www.zaragoza.es/sede/servicio/urbanismo-infraestructuras/equipamiento/aparcamiento-bicicleta.json'

response = requests.get(url)


if response.status_code == 200:
    data = response.json()
    print(data)
    print('OK')
else:
    print(f"[-] Error: {response.status_code}")
