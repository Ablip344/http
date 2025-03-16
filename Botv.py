import requests
import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# AUTOR: Pablo Gracia
# Se deberan instalar todas las librerías requeridas


# [!] ATENCIÓN - Script personalizado, no funcionara, si no se adapta adecuadamente

#_________________________________________________________________________
# El script analiza la información de los clientes, almacenando su usuario,
# enlace de este, la ubicación de donde provienen, si existe, etc

# El propio script almacena toda la información en una hoja de cálculo
# de Google, mediante el uso de su API gratuita 

# Este script estña hecho de manera que necesita ciertos requisitos para funcionar
#   - Descargar un webdriver para chrome el cual se encontrará en el enlace de abajo
#          ENLACE: https://googlechromelabs.github.io/chrome-for-testing/
#   - Se deberá cambiar la ruta de acceso al driver

# Además, y debido a ser un script personalizado, deberá tener una sesión iniciada
# en la página de vinted.es

# Finalmente, y algo muy importante, el propio script selecciona una sesión de usuario especifica
# en chrome, lo cual, si no se revisa, puede dar errores, o seleccionar un usuario incorrecto


# EJECUCIÓN
# Deberán cerrarse todas las pestañas de chrome abiertas, de lo contrario el script no funcionará


#_________________________________________________________________________


def inicio():
    chrome_options = Options()

    profile_path = r"C:\Users\Pablo\AppData\Local\Google\Chrome\User Data"
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument("profile-directory=Default")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    service = Service(r"C:\Users\Pablo\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def obtener_cookies(driver):
    cookies = driver.get_cookies()
    return {cookie["name"]: cookie["value"] for cookie in cookies}


def usuarios(driver):
    driver.get("https://www.vinted.es/member/notifications")

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    user_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-ch="wnt"]')
    usuarios = [user_link.text for user_link in user_links]
    enlaces = [user_link.get_attribute("href") for user_link in user_links]
    cookies = obtener_cookies(driver)
    driver.quit()

    ubicaciones = gps(enlaces, cookies)
    fin(usuarios, enlaces, ubicaciones)


def gps(hrefs, cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    def obtener_ubicacion(href):
        try:
            response = requests.get(href, headers=headers, cookies=cookies)
            soup = BeautifulSoup(response.content, "html.parser")
            ubicacion_element = soup.select_one('div[data-testid="profile-location-info--content"]')
            if ubicacion_element:
                return ubicacion_element.text.strip()
            return "Ubicación no encontrada"
        except Exception as e:
            print(f"Error al procesar {href}: {e}")
            return "Error al obtener ubicación"

    ubicaciones = []
    for href in hrefs:
        ubicacion = obtener_ubicacion(href)
        if ubicacion == "Ubicación no encontrada":
            # Respaldo con Selenium si Requests falla
            ubicacion = respaldo_selenium(href)
        ubicaciones.append(ubicacion)

    return ubicaciones


def respaldo_selenium(href):
    try:
        driver = inicio()
        driver.get(href)
        time.sleep(3)
        ubicacion_element = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="profile-location-info--content"]')
        ubicacion = ubicacion_element.text.strip()
        driver.quit()
        return ubicacion
    except Exception as e:
        print(f"Error con Selenium en {href}: {e}")
        return "Error al obtener ubicación con Selenium"


def fin(users, hrefs, ubicaciones):
    print("\n--- Datos Finales ---\n")
        # Configuración de las credenciales y acceso a la hoja
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    # Identificar la hoja de cálculo y la hoja específica
    sheet_ventas='1A7ulQcC-rZfrBGcqNABn3r6-noVOHQQNSKfnWxy6wOo'  # ID de la hoja de cálculo
    sheet_subidas='1h5SsdBhMSB5cWYBxrgwKMH47X94nucFeSXcGL-wjiZw'
    sheet_users='1rLwzNVcxRVdoaS_bo4Oq_xZspePlVSPkqvmZ36C04f0'
    workbook = client.open_by_key(sheet_users)
    ventas_sheet_name = "Users"

    # Verificar si la hoja existe
    worksheet_list = list(map(lambda x: x.title, workbook.worksheets()))
    if ventas_sheet_name not in worksheet_list:
        print("La hoja de trabajo 'Ventas' no existe. Verifica el nombre.")
        exit()

    sheet = workbook.worksheet(ventas_sheet_name)
    for user, href, ubicacion in zip(users, hrefs, ubicaciones):
        print(f"Usuario: {user}, Enlace: {href}, Ubicación: {ubicacion}")
        data=[[user,ubicacion,href]]
        send(data,sheet)


def send(new_data,sheet):
    # Añadir los datos al final de la hoja
    for row in new_data:
        sheet.append_row(row)
    print("Nuevas filas añadidas correctamente.")

usuarios(inicio())