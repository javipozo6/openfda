#Importamos los siguientes módulos que nos serán de utilidad para poder leer la información de la página web
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexión con la página solicitada
conn.request("GET", "/drug/label.json?&limit=10", None, headers) #GET: enviamos solicitud
r1 = conn.getresponse() #Obtenemos la respuesta de la solicitud enviada
if r1.status == 404: #Comprobamos si se ha podido encontrar el recurso correctamente (código 200), o si no se ha podido (código 404)
    print("ERROR, recurso no encontrado.")
    exit(1)
print(r1.status, r1.reason) #Imprimimos el código de estado de la respuesta
datos_raw = r1.read().decode("utf-8") #Convertimos la información para que sea legible
conn.close()

info = json.loads(datos_raw)['results'] #Convertimos la información a json

for elem in range(len(info)): #Con esto iteramos sobre los datos de los 10 medicamentos diferentes que queremos
    print('El id del medicamento es:', info[elem]['id']) #Imprimimos todas las id de los medicamentos

