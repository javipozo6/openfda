#Importamos los siguientes módulos que nos serán de utilidad para poder leer la información de la página web
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecemos conexión con la página solicitada
conn.request("GET", "/drug/label.json", None, headers) #GET: enviamos solicitud
r1 = conn.getresponse() #Obtenemos la respuesta de la solicitud enviada

if r1.status == 404: #Comprobamos si se ha podido encontrar el recurso correctamente (código 200), o si no se ha podido (código 404)
    print("ERROR, recurso no encontrado.")
    exit(1)

print(r1.status, r1.reason) #Imprimimos el código de estado de la respuesta
datos_raw = r1.read().decode("utf-8") #Convertimos la información para que sea legible
conn.close()

info = json.loads(datos_raw)['results'][0] #Convertimos la información a json

print('La id del producto es:', info['id']) #Accedemos a la id del producto
print("El propósito del producto es:", info['purpose'][0]) #Accedemos al 'purpose' del producto
print('El nombre del fabricante del producto es:', info['openfda']['manufacturer_name'][0]) #Accedemos al nombre del fabricante del producto