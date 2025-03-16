import requests
import csv
import time
from datetime import datetime

id_est = 1132 
url = f'https://www.zaragoza.es/sede/servicio/urbanismo-infraestructuras/equipamiento/aparcamiento-bicicleta.json?=&id={int(id_est)}'
 

def get_estacion():
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get('result',[])
        data=data[0]
        
        return {
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "id": data.get("id", "N/A"),
                    "bicis_disponibles": data.get("plazas", "N/A"),
                    "anclajes_disponibles": data.get("anclajes", "N/A")
                }
    return None

def guardar_en_csv():
    archivo = "datos_estacion.csv"

    with open(archivo, "a", newline="", encoding="utf-8") as file:
        escritor = csv.writer(file)
        
        if file.tell() == 0:
            escritor.writerow(["Fecha de registro", "ID Estación", "Bicis disponibles", "Anclajes disponibles"])
        
        while True:
            datos = get_estacion()
            if datos:
                escritor.writerow([datos["fecha"], datos["id"], datos["bicis_disponibles"], datos["anclajes_disponibles"]])
                print(f"📌 Datos guardados: {datos}")
            else:
                print("⚠ No se encontraron datos para la estación.")
            
            time.sleep(60)

guardar_en_csv()
