import http.server
import http.client
import json
import socketserver

PORT = 8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # Declaramos algunas variables
    API_URL = "api.fda.gov"
    API_EVENT = "/drug/label.json"
    SEARCH_DRUG = '&search=active_ingredient:'
    SEARCH_COMPANY = '&search=openfda.manufacturer_name:'

    def get_html(self):
        # Definimos la estructura que tendrá nuestro formulario en html
        html = """
            <html>
                <head>
                    <center><title>OpenFDA App</title></center>
                </head>
                <body align=center style='background-color: red'>
                    <h1>OPENFDA </h2>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>  
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    <br>

                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <br>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    <br>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <br>
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                    <br>
                    <br>
                    <h3> Autor: Javier Pozo Ocampo </h3> 

                </body>
            </html>
                """
        return html

    def get_data(self, lista):
        # Definimos la estructura de nuestro html al hacer llamada a alguno de los parámetros anteriores
        data_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body style='background-color: blue'>
                                    <h2> Los datos obtenidos son los siguientes: </h2>
                                        <ul>
                            """
        for i in lista:  # Iteramos sobre los elementos de la lista, y los escribimos en forma de lista en html
            data_html += "<li>" + i + "</li>"

        data_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return data_html

    def get_results(self, limit=10):
        conn = http.client.HTTPSConnection(self.API_URL)  # Establecemos conexión con la página solicitada
        conn.request("GET", self.API_EVENT + "?limit=" + str(limit))  # GET: enviamos solicitud
        print(self.API_EVENT + "?limit=" + str(limit))
        r1 = conn.getresponse()  # Obtenemos la respuesta de la solicitud enviada
        print(r1.status, r1.reason)  # Imprimimos el código de estado de la respuesta
        data_raw = r1.read().decode("utf8")  # Convertimos la información para que sea legible
        data = json.loads(data_raw)  # Convertimos la información a json
        resultados = data['results']
        return resultados

    def do_GET(self):
        recurso = self.path.split("?")  # Separamos el recurso a partir del ? que aparezca
        if len(recurso) > 1:
            partes = recurso[1]
        else:
            partes = ""

        limit = 1  # Colocamos el limite en 1 por defecto

        # Obtenemos las partes del recurso
        if partes:
            parse = partes.split("=")  # Separamos las partes del recurso que queremos
            if parse[0] == "limit":
                limit = int(parse[1])
                print("Limit: {}".format(limit))
        else:
            print("No hay parámetros adicionales")

        if self.path == '/':  # Construímos la pagina de inicio a partir de esta condición (que el recurso sea una /)
            # La primera linea del mensaje de respuesta es el status. Indicamos que OK
            self.send_response(200)
            # En las siguientes lineas de la respuesta colocamos las cabeceras necesarias para que el cliente entienda el contenido que le enviamos (en HTML)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.get_html()
            self.wfile.write(bytes(html, "utf8"))  # Escribimos la pagina en html llamando a la funcion creada anteriormente
        elif 'listDrugs' in self.path:  # Si el recurso solicitado es 'listDrugs':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicamentos = []  # Creamos una lista para almacenar todos los medicamentos
            info = self.get_results(
                limit)  # Tomamos los resultados obtenidos en la función creada anteriormente (limit=1 por defecto)
            for elem in info:  # Iteramos sobre los elementos de los resultados obtenidos anteriormente
                if ('generic_name' in elem[
                    'openfda']):  # Si existe ese valor, almacenamos los datos que hay en él en la lista creada
                    medicamentos.append(elem['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Unknown')  # Si no existe, añadimos que el nombre el medicamento es desconocido
            medicamentos_html = self.get_data(medicamentos)  # Para escribir los medicamentos en html llamamos a la función creada anteriormente

            self.wfile.write(bytes(medicamentos_html, "utf8"))  # Escribimos los medicamentos en html
        elif 'listCompanies' in self.path:  # Si el recurso solicitado es 'listCompanies':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []  # Creamos una lista para almacenar todos los nombres de empresas
            info = self.get_results(limit)  # Tomamos los resultados obtenidos en la función creada anteriormente (limit=1 por defecto)
            for elem in info:  # Iteramos sobre los elementos de los resultados obtenidos anteriormente
                if ('manufacturer_name' in elem['openfda']):  # Si existe ese valor, almacenamos los datos que hay en él en la lista creada
                    companies.append(elem['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Unknown')  # Si no existe, añadimos que el nombre el medicamento es desconocido
            companies_html = self.get_data(companies)  # Para escribir las empresas en html llamamos a la función creada anteriormente

            self.wfile.write(bytes(companies_html, "utf8"))  # Escribimos las empresas en html
        elif 'listWarnings' in self.path:  # Si el recurso solicitado es 'listWarnings':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []  # Creamos una lista para almacenar todos los nombres de advertencias
            info = self.get_results(limit)  # Tomamos los resultados obtenidos en la función creada anteriormente (limit=1 por defecto)
            for elem in info:  # Iteramos sobre los elementos de los resultados obtenidos anteriormente
                if ('warnings' in elem):  # Si existe ese valor, almacenamos los datos que hay en él en la lista creada
                    warnings.append(elem['warnings'][0])
                else:
                    warnings.append('Unknown')  # Si no existe, añadimos que el nombre el medicamento es desconocido
            warnings_html = self.get_data(warnings)  # Para escribir las advertencias en html llamamos a la función creada anteriormente

            self.wfile.write(bytes(warnings_html, "utf8"))  # Escribimos las advertencias en html
        elif 'searchDrug' in self.path:  # Si el recurso solicitado es 'searchDrug':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10  # El limite será 10 en este caso
            drug = self.path.split('=')[1]  # Dividimos el recurso y nos quedamos con el 2º valor

            drugs = []  # Creamos una lista para almacenar todos los nombres de medicamentos
            conn = http.client.HTTPSConnection(self.API_URL)  # Establecemos conexión con la página solicitada
            conn.request("GET",self.API_EVENT + "?limit=" + str(limit) + self.SEARCH_DRUG + drug)  # GET: enviamos solicitud
            r1 = conn.getresponse()  # Obtenemos la respuesta de la solicitud enviada
            datos_raw = r1.read().decode('utf8')  # Convertimos la información para que sea legible

            info_drugs = json.loads(datos_raw)['results']  # Convertimos la información a json

            for elem in info_drugs:  # Iteramos sobre los elementos de los resultados obtenidos anteriormente
                if ('generic_name' in elem['openfda']):  # Si existe ese valor, almacenamos los datos que hay en él en la lista creada
                    drugs.append(elem['openfda']['generic_name'][0])
                else:
                    drugs.append('Unknown')  # Si no existe, añadimos que el nombre el medicamento es desconocido

            drugs_html = self.get_data(drugs)  # Para escribir los medicamentos en html llamamos a la función creada anteriormente
            self.wfile.write(bytes(drugs_html, "utf8"))  # Escribimos los medicamentos en html
        elif 'searchCompany' in self.path:  # Si el recurso solicitado es 'searchCompany':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limit = 10  # El limite será 10 en este caso
            company = self.path.split('=')[1]  # Dividimos el recurso y nos quedamos con el 2º valor
            companies = []  # Creamos una lista para almacenar todos los nombres de empresas
            conn = http.client.HTTPSConnection(self.API_URL)  # Establecemos conexión con la página solicitada
            conn.request("GET", self.API_EVENT + "?limit=" + str(limit) + self.SEARCH_COMPANY + company)  # GET: enviamos solicitud
            r1 = conn.getresponse()  # Obtenemos la respuesta de la solicitud enviada
            datos_raw = r1.read().decode('utf8')  # Convertimos la información para que sea legible

            info_companies = json.loads(datos_raw)['results']  # Convertimos la información a json

            for elem in info_companies:  # Iteramos sobre los elementos de los resultados obtenidos anteriormente
                companies.append(elem['openfda']['manufacturer_name'][0])  # Si existe ese valor, almacenamos los datos que hay en él en la lista creada
            compañias_html = self.get_data(companies)  # Para escribir las empresas en html llamamos a la función creada anteriormente
            self.wfile.write(bytes(compañias_html, "utf8"))  # Escribimos las empresas en html
        elif 'secret' in self.path:  # Si el recurso solicitado es 'secret':
            self.send_response(401)  # Nos devolverá el codigo 401 (Unauthorized)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')  # Se envía la siguiente cabecera
            self.end_headers()
        elif 'redirect' in self.path:  # Si el recurso solicitado es 'redirect':
            self.send_response(301)  # Nos devolverá el código 301
            self.send_header('Location', 'http://localhost:' + str(PORT))  # Se envía esta cabecera, que nos devuelve a la página principal
            self.end_headers()
        else:
            self.send_response(404)  # Nos devolverá el código 404 (error)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("ERROR 404. Se desconoce el siguiente recurso solicitado: '{}'.".format(self.path).encode())  # Se escribe un mensaje de error por pantalla
        return


socketserver.TCPServer.allow_reuse_address = True  # Para no tener que cambiar de puerto constantemente

# El servidor comienza aqui
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# Se configura el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)

    # Entra en el bucle principal
    # Las peticiones se atienden desde nuestro manejador
    # Cada vez que se ocurra un "GET" se invoca al metodo do_GET del manejador

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")