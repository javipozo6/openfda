#Importamos los siguientes módulos que nos serán de utilidad para poder leer la información de la página web
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
datos_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(datos_raw)['results'][0]

print('La id del producto es:', info['id']) #Accedemos a la id del producto
print("El propósito del producto es:", info['purpose'][0]) #Accedemos al 'purpose' del producto
print('El nombre del fabricante del producto es:', info['openfda']['manufacturer_name'][0]) #Accedemos al nombre del fabricante del producto