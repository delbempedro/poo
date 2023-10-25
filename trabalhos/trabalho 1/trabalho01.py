#importa o módulo sys
import sys

#lê a linha de comando no terminal
arquivo = sys.argv[1]

#abre o arquivo dito no terminal
f = open(arquivo,'r')

#lê as 3 primeiras linhas do arquivo e pega as informações de dimensão do arquivo, ignorando o comentário
dim = list(f.readlines(3))
vetor = 1
if '#' in dim[1]:
	width,height = f.readline().split()
else:
	width,height = dim[vetor].split()
width,height = int(width),int(height)

#lê o número de bins do arquivo
bins = int(sys.argv[-1])

#lẽ o valor máximo do arquivo
maxval = list(f.readlines(2))
maxval = int(maxval[0]) + 1 #soma um a maxval para permitir que o intervalo final seja aberto

#implimenta o programa que será executado caso as condições passem pelos testes de erro
def programa():
	#determina o tamnho do intervalo
	tamanho = maxval/bins
	
	#cria uma lista com os intervalos
	intervalos = []
	for i in range(0,bins+1):
		intervalos.append(tamanho*i)
		
	#cria uma lista com os valores da imagem
	valores = f.read().split()

	#lista com o número de pixels em cada intevalo
	pixels = [0]*bins

	#calcula quantos pixels estão em cada intervalo
	for indice in range(len(intervalos)):
		if len(intervalos) >= indice+1:
			for valor in valores:
				valor = int(valor)
				if intervalos[indice] <= valor < intervalos[indice + 1]:
					pixels[indice] += 1
	
	#escreve os resultados na tela
	total = width*height
	for interv in range(0,len(intervalos)):
		if interv + 1 < len(intervalos):
			primeirointerv = str("%.2f"%intervalos[interv])
			segundointerv = str("%.2f"%intervalos[interv+1])
			pixelsnumero = str(pixels[interv])
			pixelsrazao = str("%.5f"%(pixels[interv]/total))
			print('['+primeirointerv+', '+segundointerv+') '+pixelsnumero+' '+pixelsrazao)

#testa se o número de bins é executável (<=masxal)
if maxval < bins:
	maxval -= 1 #tira um de maxval para que ele fique com o valor original
	print("Erro: número de bins pedido",bins,", mas ",maxval," é o valor máximo de intensidade na imagem.")
elif bins <= 0:
	print("Erro: não é possível gerar",bins,"bins.")
else: #o programa pode proseguir
	programa()
