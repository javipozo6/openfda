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

print('The product id is', info['id'])
print("The purpose of the product is", info['purpose'][0])
print('The manufacturer name is', info['openfda']['manufacturer_name'][0])