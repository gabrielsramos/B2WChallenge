#!/usr/bin/env python

import unittest



#Funcao que resolve o desafio "Hell triangle"
def hellTriangle(entrada):

	#Inicializa com 0 a variavel que tera o resultado final
	sum = 0
	index = -1

	#Percorre cada camada do triangulo 
	for vec in entrada:
		if index == -1:
			sum = sum + vec[0]
			index = 0
		else:
			#Percorre a partir da segunda camada, verificando o maior numero dos 2 vizinhos e somando ao total, armazena o indice para saber os proximos vizinhos na camada seguinte
			if vec[index] > vec[index+1]:
				sum = sum + vec[index]
			else:
				sum = sum + vec[index+1]
				index = index+1
				
	return sum

#Classe que realiza o teste na funcao principal
class TestUnit(unittest.TestCase):
	def test_(self):
			entrada_teste = [[6],[3,5],[9,7,1],[4,6,8,4]]
			self.assertEqual(26,hellTriangle(entrada_teste))
		
		

#Executa o teste
unittest.main()