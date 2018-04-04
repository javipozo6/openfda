#Importamos los siguientes módulos que nos serán de utilidad para poder leer la información de la página web
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
datos_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(datos_raw)['results']

for elem in range(len(info)): #Con esto iteramos sobre los datos de los 10 medicamentos diferentes que queremos
    print('El id del medicamento es:', info[elem]['id']) #Imprimimos todas las id de los medicamentos

