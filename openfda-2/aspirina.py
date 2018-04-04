import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json/?search=active_ingredient:acetylsalicylic&limit=100", None, headers) #Realizamos la búsqueda comprobando el principio activo y poniendo un límite de 100
r1 = conn.getresponse()
print(r1.status, r1.reason)
datos_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(datos_raw)['results']


for elem in range(len(info)): #Con esto iteramos sobre los datos de los diferentes medicamentos que tenemos
    print('El id del medicamento es:', info[elem]['id']) #Accedemos al id del medicamento
    #Si el nombre del fabricante es desconocido, saltará un KeyError, asi que lo evitamos con un try-except
    try:
        print('Su fabricante es:', info[elem]['openfda']['manufacturer_name'][0],'\n')
    except KeyError:
        print('El nombre del fabricante no está disponible\n')