#Importamos los siguientes módulos que nos serán de utilidad para nuestro objetivo
import http.server
import socketserver
import http.client
import json

PORT = 8000


headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
datos_raw = r1.read().decode("utf-8")
medicamentos = [] #Se crea una lista para almacenar los nombres de los medicamentos
conn.close()

info = json.loads(datos_raw)['results']

for i in range(len(info)):#Con esto iteramos sobre los datos de todos los diferentes medicamentos
    if info[i]['openfda']:#Si esto existe, entonces entramos para coger el nombre del medicamento
        if len(medicamentos) <= 9: #Si ya hay 10 medicamentos almacenados en la lista, no queremos almacenar más
            medicamentos.append(info[i]['openfda']['generic_name'][0]) #Añadimos los medicamentos a la lista con la función append
    else:
        continue


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una peticion GET por HTTP. El recurso que nos solicitan se encuentra en self.path
    def do_GET(self):
        #La primera linea del mensaje de respuesta es el status. Indicamos que OK

        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las cabeceras necesarias para que el cliente entienda el contenido que le enviamos (en HTML)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #Aquí escribiremos el mensaje que queremos mostrar en html
        message = """<html>
        <body>
        <ol>"""
        message += "<h2>Los medicamentos son:</h3>"
        for elem in medicamentos: #Iteramos sobre los elementos de la lista, y los escribimos en forma de lista ordenada (ol) en html
            message += "<li type='disc'>" + elem + '</li>'
        message += """</ol>
        </body>
        </html>"""

        self.wfile.write(bytes(message, "utf8"))

        return


# El servidor comienza aqui
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

#Se configura el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)

    #Entra en el bucle principal
    #Las peticiones se atienden desde nuestro manejador
    #Cada vez que se ocurra un "GET" se invoca al metodo do_GET del manejador

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")