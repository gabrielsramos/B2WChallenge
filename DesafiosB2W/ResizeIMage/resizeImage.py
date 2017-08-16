#!/usr/bin/env python
import web
import urllib.request, json , urllib
from PIL import Image
from pymongo import MongoClient
import os


#Cria conexao com o banco de dados
cliente = MongoClient('localhost', 27017)

#Seleciona o banco a ser usado
banco = cliente['Gabriel']

#Cria a colecao que sera usada para armazenar as imagens
db_images = banco['images']

#Possui as urls a serem usadas e suas funcoes
urls = (
	'/image', 'lista_imagens',
)

app = web.application(urls, globals())

class lista_imagens:        
	def GET(self):
		#Carrega as imagens originais em json
		with urllib.request.urlopen("http://54.152.221.29/images.json") as url:
			data = json.loads(url.read().decode())
		#Percorre o json, e para cada imagem realiza as alteracoes de tamanho
		for i,doc in enumerate(data['images']):
			f = open('static/original_'+str(i)+'.jpg','wb')
			f.write(urllib.request.urlopen(doc.get('url')).read())
			f.close()
			#Salva a imagem original
			im = Image.open("static/original_"+str(i)+".jpg")
			
			#Realiza as alteracoes de tamanho, e salva em uma pasta static dentro do server
			out = im.resize((320,240))
			out.save("static/"+str(i)+"_pequena.jpg","JPEG")
			
			out = im.resize((384,288))
			out.save("static/"+str(i)+"_media.jpg","JPEG")
			
			out = im.resize((640,480))
			out.save("static/"+str(i)+"_grande.jpg","JPEG")
			
			#Salva no banco as urls das imagens modificadas e a original
			post = {"original" : "localhost:8080/static/original_"+str(i)+".jpg",
					"pequena" : "localhost:8080/static/"+str(i)+"_pequena.jpg",
					"media" : "localhost:8080/static/"+str(i)+"_media.jpg",
					"grande" : "localhost:8080/static/"+str(i)+"_grande.jpg"}
			db_images.insert_one(post)
			
		#Retorna todos os objetos do banco
		cursor = db_images.find({})
		#Formata em json (dentro de uma string) para imprimir na pagina
		result = '{\r\n\t"images": [\r\n'
		for col in cursor:
			result = result+"\t\t"+str(col)+",\r\n"
		result = result +"\t]\r\n}"
		return result
		
	

if __name__ == "__main__":
	app.run()
	
	
	
	