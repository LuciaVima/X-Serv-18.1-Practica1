#Lucia Villa Martinez
import webapp
import csv
import urllib
#-*- coding: utf-8 -*-


class App(webapp.webApp): 
	
	diccionario_URLs = {}
	diccionario_GET = {}
	try:
		with open('redireccion.csv') as csvfile:
			leer = csv.reader(csvfile)
			for row in leer:
				Url_corta = row[0]
				Url_larga = row[1]
				diccionario_URLs[Url_larga] = Url_corta

		with open('redireccion.csv') as csvfile:
			leer = csv.reader(csvfile)
			for row in leer:
				Url_corta = row[0]
				Url_larga = row[1]
				diccionario_GET[Url_corta] = Url_larga

	except:
		cvsfile = open('redireccion.csv', 'w') 
		csvfile.close()
	
	def parse(self, request):
		metodo = request.split(' ',2)[0]
		try:
			recurso = request.split(' ',2)[1]
		except:
			recurso = "/"
		try:
			cuerpo = request.split('\r\n\r\n')[1]
		except IndexError:
			cuerpo = ""
		return metodo, recurso, cuerpo

	def process(self, peticion):
		metodo, recurso, cuerpo = peticion
		if metodo == "GET":
			if (recurso != '/'):
				urlabuscar = 'http://localhost:1234' + str(recurso)
				try:
					urlaredirigir = self.diccionario_GET[urlabuscar]
					httpCode = "200 OK"
					htmlBody = '<html><head><meta http-equiv="Refresh" content="5;url='+ urlaredirigir +'"></head>' \
						+ "<body><h1> Espere, va a ser redirigido en 5 segundos... " \
						+ "</h1></body></html>"
				except KeyError:
					httpCode = "200 OK"
					htmlBody = "<html><body>" \
						+ 'ERROR: Recurso no valido. Vuelva a intentarlo.' \
						+ "</body></html>"

				
			else:

				httpCode = "200 OK"
				htmlBody = "<html><body>"  \
					+ '<form method="POST" action="">' \
					+ 'URL: <input type="text" name="url"><br>' \
					+ '<input type="submit" value="Enviar"><br>' \
					+ '</form>' \
					+ "</body></html>"
			
				for clave, valor in self.diccionario_URLs.iteritems(): 
					htmlBody = htmlBody + '<html><body><a href="'+ clave +'">' + clave + ' </a></br></body></html>' \
					+ '<html><body><a href="'+ valor +'">'+ valor + ' </a></br></body></html>'
				
			
		elif metodo == "PUT" or metodo == "POST":
			if cuerpo != "":
				
				urlparaacortar = cuerpo.split("=")[1]
				urlparaacortar = urllib.unquote(urlparaacortar).decode('utf8')
				http = urlparaacortar.split("://")[0]

				if (http != 'http') and (http != 'https'):
					urlparaacortar = 'https://' + urlparaacortar

				try:
					urlcorta = self.diccionario_URLs[urlparaacortar]
					httpCode = "200 OK"
					htmlBody = "<html><body><h1> Esta URL ya ha sido acortada " \
					+ "</h1></body></html>" \
					+ "\r\n" \
					+'<html><body><a href="'+ urlparaacortar +'">' + urlparaacortar + ' </a></br></body></html>'\
					+ '<html><body><a href="'+ urlcorta +'">'+ urlcorta + ' </a></br></body></html>'
					
				except KeyError:
					contador = len(self.diccionario_URLs)
					urlnuevacorta = 'http://localhost:1234/' + str(contador)
					self.diccionario_URLs[urlparaacortar] = urlnuevacorta
					self.diccionario_GET[urlnuevacorta] = urlparaacortar
					with open ('redireccion.csv', 'a') as csvfile:
						escribir = csv.writer(csvfile)
						escribir.writerow([urlnuevacorta,urlparaacortar])
					httpCode = "200 OK"
					htmlBody = "<html><body> Se ha acortado la URL de forma correcta</br>" \
					+'<a href="'+ urlparaacortar +'">' + urlparaacortar + ' </a></br>'\
					+ '<a href="'+ urlnuevacorta +'">'+ urlnuevacorta + ' </a></br></body></html>'

			else:
				httpCode = "200 OK"
				htmlBody = "<html><body>" \
				+ 'ERROR: No ha introducido una URL valida para acortar.' \
				+ "</body></html>"
				
		else:
			httpCode = "450 Method Not Allowed"
			htmlBody = "Go Way!"
		return (httpCode, htmlBody)



if __name__ == "__main__":
	try:
		myWebApp = App("localhost", 1234)
	except KeyboardInterrupt:
		print "Gracias por utilizar la aplicacion. Espero que vuelva pronto."


