import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json/?search=active_ingredient:acetylsalicylic&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
datos_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(datos_raw)['results']


for elem in range(len(info)):
    print('El id del medicamento es:', info[elem]['id'])
    try:
        print('El nombre del fabricante es:', info[elem]['openfda']['manufacturer_name'],'\n')
    except KeyError:
        print('El nombre del fabricante no está disponible\n')