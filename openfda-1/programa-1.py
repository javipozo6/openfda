import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
datos_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(datos_raw)

print('The product id is', info['results'][0]['id'])
print("The purpose of the product is", info['results'][0]['purpose'])
print('The manufacturer name is', info['results'][0]['openfda']['manufacturer_name'])