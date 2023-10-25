import argparse
from math import hypot

class Image(): 
    def __init__(self,magicnumber,width,height,maxval,matrix,*args,**kargs):
        self._valores = matrix
        self._width = width
        self._height = height
        self._magicnumber = magicnumber
        self._maxval =  maxval
        self._histograma = histograma(matrix)
        self._T = args
        self._mean = mean(self._valores,self._width,self._height)
        self._median = median(self._valores)
    
    def get_valores(self):
        return self._valores
    
    def get_T(self):
        return self._T[0]
    
    def get_median(self):
        return self._median
    
    def get_mean(self):
        return self._mean
    
    def get_magicnumber(self):
        return self._magicnumber
    
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_maxval(self):
        return self._maxval
    
    def getmatrix(self):
        return self._valores
    
    def thresholding(self,t=127):
        #aplica thresholding
        self._T = t
        newmatrix = thres(self._valores,self._T)

        return Image(self._magicnumber,self._width,self._height,255,newmatrix)
    
    def sgt(self,dt=1):
        
        med = media(self._valores,self._width,self._height) #calcula o valor médio dos pixels
        newt = med #salva a média como novo parâmtro para o thresholding
        oldt = 1000 #valor arbitrário, escolhido apenas para definir o oldt de modo que o loop a seguir funcione

        while dt < abs(newt-oldt): #calcula um novo t até que a diferença entre oldt e newt seja menor que dt
            
            oldt = newt #salva o valor de t atual, em oldt, antes de alterá-lo
            newt = calcularnovot(self._valores,oldt) #calcula um novo valor para o parâmetro t
        
        nmatrix = thres(self._valores,newt)
        
        self._T = newt
        
        return Image(self._magicnumber,self._width,self._height,255,nmatrix,self._T)
            
    def mean(self,k=3):
        
        newmatrix,maxval = meanmatrix(self._valores,k,self._width,self._height)

        return Image(self._magicnumber,self._width,self._height,maxval,newmatrix)
        
    def median(self,k=3):
        
        newmatrix,maxval = medianmatrix(self._valores,k,self._width,self._height)
        
        return Image(self._magicnumber,self._width,self._height,maxval,newmatrix)

    def sobel(self):
        
        matrix1 = kernel(self._valores,[1,0,-1,2,0,-2,1,0,-1],self._width,self._height)
        matrix2 = kernel(self._valores,[1,2,1,0,0,0,-1,-2,-1],self._width,self._height)
        newmatrix,maxval = sobel(matrix1,matrix2,self._width,self._height)
        newmatrix = normalizacao(newmatrix,maxval,self._width,self._height)
    
        return Image(self._magicnumber,self._width,self._height,255,newmatrix)

    
def geral(): #executa a totalidade do código
    try: #tenta executar o programa
        arquivo, metodos, argumentos, savesite = leitura() #leitura do arquivo
        
        oldimagem = leimagem(arquivo) #cria imagem com as informações tratadas
        imagem = oldimagem
        
        contador = 0
        for metodo in metodos:

            if metodo == 'thresholding':
                imagem = imagem.thresholding(int(argumentos[contador+1]))
                contador += 2
                print('passei pelo thresholding')
                
            elif metodo == 'sgt':
                imagem = imagem.sgt(int(argumentos[contador+1]))
                printinformacoes(imagem,oldimagem) #faz o print das informações
                contador += 2
                print('passei pelo sgt')
            
            elif metodo == 'sobel':
                imagem = imagem.sobel()
                print('passei pelo sobel')

                
            elif metodo == 'mean':
                imagem = imagem.mean(int(argumentos[contador+1]))
                contador += 2
                print('passei pelo mean')
                
            else:
                imagem = imagem.median(int(argumentos[contador+1]))
                contador += 2
                print('passei pelo median')
                
        print(compara_imagens(imagem,'exemplos-t3/output/mule-sobel-sgt-1.pgm'))
        
        salvar(imagem,arquivo,metodos,savesite)
        
    except ArgumentoInvalido: #se o parâmetro não corresponder ao método, apresenta a mensagem de erro
        print("O parâmetro fornecido não corresponde ao método fornecido, tente novamente!")
        
def leitura(): #faz a leitura da linha de comando
    parser = argparse.ArgumentParser(description = 'Leitura da linha de comando') #cria o objeto que será responsável por analisar os argumentos passados pelo terminal
    
    #salva os parâmetros
    #como funciona: pega '--something', faz 'action =' e salva em 'dest =' com valor default 'default =', 'required =' diz se o valor é obrigatório, 'help =' determina o que será impresso caso o usuário dê o comando '-h'
    parser.add_argument('--imgpath', action = 'store', dest = 'arquivo',
                        required = True, help = 'O arquivo que deseja-se tratar com o caminho até ele' )
    parser.add_argument('--op', action = 'store', dest = 'metodo',
                        required = True, help = 'O método a ser utilizado') #MODIFICAR PARA PODER LER VÁRIOS MÉTODOS EM SEQUÊNCIA
    parser.add_argument('--t', action = 'store', dest = 'arg1', default = None,
                        required = False, help = 'O parâmetro a ser utilizado')
    parser.add_argument('--dt', action = 'store', dest = 'arg2', default = None,
                        required = False, help = 'O parâmetro a ser utilizado')
    parser.add_argument('--k', action = 'store', dest = 'arg3', default = None,
                        required = False, help = 'O parâmetro a ser utilizado')
    parser.add_argument('--outputpath', action = 'store', dest = 'savesite',
                        required = False, help = 'Onde o arquivo será salvo')

    #cria um objeto com os parâmetros passados pelo usuário
    arguments = parser.parse_args()
    auxiliar = tratametodos(arguments.metodo)
    metodos, args = auxiliar[0], auxiliar[1]
    
    '''
    #testa se os parâmetro corresponde ao método
    if (arguments.metodo == 'thresholding' and arguments.arg1 == None) or (arguments.metodo == 'sgt' and arguments.arg2 == None) or ( (arguments.metodo == 'mean' or arguments.metodo == 'median' )and arguments.arg3 == None):
        raise ArgumentoInvalido()
    else: #se o parâmetro corresponde ao método, salva 
        if arguments.metodo == 'thresholding':
            arg = int(arguments.arg1)
        elif arguments.metodo == 'sgt':
            arg = int(arguments.arg2)
        elif arguments.metodo == 'mean' or arguments.metodo == 'median':
            arg = int(arguments.arg3)
        else:
            arg = None
    '''
    return arguments.arquivo, metodos, args, arguments.savesite

class ArgumentoInvalido(ValueError):
    pass

def tratametodos(lista): #separa as informações de --op em metodos e argumentos
    metodos = []
    args = []
    lista = lista.split(',')
    for item in lista:
        if item == 'thresholding' or item == 'sgt' or item == 'mean' or item == 'median' or item == 'sobel':
            metodos.append(item)
        else:
            args.append(item)

    return metodos, args

def salvar(image,arquivo,metodos,savesite):
    
    imagem = str(arquivo.split('/')[-1].split('.')[0]) #separa o nome do arquivo do diretório
    
    nomedoarquivo = str(imagem)
    for metodo in metodos:
        nomedoarquivo = nomedoarquivo + "-" + str(metodo)
    
    #pega as informacoes pertinentes para a escrita do arquivo
    magicnumber = image.get_magicnumber()
    width = image.get_width()
    height = image.get_height()
    maxval = image.get_maxval()
    valores = image.get_valores() 
    
    if savesite: #verifica se savesite foi fornecido
        nomedoarquivo_ = savesite+'/'+nomedoarquivo+'.pgm'
    else:
        nomedoarquivo_ = nomedoarquivo+'.pgm'
     
    with open(nomedoarquivo_,'w', encoding='utf-8') as file:
        file.write(magicnumber+'\n') #escreve o número mágico
        file.write(str(width)+' '+str(height)+'\n') #escreve as dimensões do arquivo
        file.write(str(maxval)+'\n') #escreve o maxval do arquivo
        
        for linha in valores:
            for value in linha:
                file.write(str(value) +' ')
            file.write('\n')
    

def compara_imagens(obtida,pretendida):
    obtida = obtida.get_valores()
    pretendida = leimagem(pretendida).get_valores()
    return obtida == pretendida

def printinformacoes(Newimage,imagem):
    print('magic_number',Newimage.get_magicnumber())
    print('dimensions',(Newimage.get_width(),Newimage.get_height()))
    print('maxval',Newimage.get_maxval())
    print('mean',imagem.get_mean())
    print('median',imagem.get_median())
    print('T',Newimage.get_T())

def leimagem(arquivo): #separa as informações do arquivo em magicnumber, widht, height, maxval e uma matrix com os valores dos pixels
    with open(str(arquivo), encoding='utf-8') as file:
        magicnumber = file.readline().strip()
        linha2 = [int(i) for i in file.readline().split()]
        if '#' in linha2:
            width,height = [int(i) for i in file.readline().split()]
        else:
            width,height = linha2
        maxval = int(file.readline().strip())
        matrix = list(file.readlines())
        
        matrix = trataamatrix(matrix)
        
        return Image(magicnumber,width,height,maxval,matrix)
    
def trataamatrix(matrix):
    matrixf = []
    for linha in matrix:
        linha = [int(i) for i in linha.strip().split()]
        matrixf.append(linha)
    
    return matrixf

def histograma(matrix):
    histo = [0]*256 #cria o histograma da matrix

    for linha in matrix:
        for value in linha:
            histo[value] += 1
            
    return histo

def thres(matrix,t):
    newmatrix = []
    for linha in matrix:
        #cria a linha para a nova imagem
        newline = []
        for value in linha: #define qual é o novo valor de acordo com o método thresholding
            if value <= t:
                newvalue = 0
            else:
                newvalue = 255
            newline.append(newvalue)
        newmatrix.append(newline)
        
    return(newmatrix)

def media(matrix,width,height): #calcula a media dos valores da imagem
    soma = 0
    for linha in matrix: #soma todos os valores dos pixels
        for value in linha:
            soma += value
    return soma/(width*height) #retorna a divisão da soma dos valores pela multiplicação das dimensões da imagem (media dos valores da imagem)

def calcularnovot(matrix,oldt): #newt = (1/2)*(m1+m2)
    #parâmteros m1 e m2 para o cálculo do novo t, onde o primeiro valor de cada lista é a soma dos valores e o segundo é quantos valores foram somados
    soma1 = [0,0]
    soma2 = [0,0]
    for linha in matrix:
        for value in linha:
            if value <= oldt:
                soma1[0] += value
                soma1[1] += 1
            else:
                soma2[0] += value
                soma2[1] += 1
    
    #calcula os valores médio abaixo e acima de oldt
    m1 = soma1[0]/soma1[1]
    m2 = soma2[0]/soma2[1]
    
    return int((1/2)*(m1+m2)) #retorna o newt

def meanmatrix(matrix,k,width,height): #monta a matrix com filtro de média k*k
    fator = int((k-1)/2) # define o fator de locomoção, número de linhas ou colunas queserão percorridas para cada "lado" do pixel central
    maxval = 0 #cria a variável que determinará o maxval
    newmatrix = [] #cria a matrix nova
    for indicelinha in range(height): #percorre todas as linhas da mterix
        linha = [] #cria a linha da matrix
        for indicecoluna in range(width): #percorre todas as colunas da mtrix
            
            #faz a soma dos valores numa região k*k
            somadosvalores = 0
            for indlinha in range(indicelinha-fator,indicelinha+fator+1): 
                for indcoluna in range(indicecoluna-fator,indicecoluna+fator+1):
                    if 0 <= indlinha < height and 0 <= indcoluna < width: #evita o erro de indice nas bordas, como estamos utilizando zero padding, basta não contablizar valores além das bordas
                        somadosvalores += matrix[indlinha][indcoluna]
            media = int(somadosvalores/(k*k))
            if media > maxval:
                maxval = media
            linha.append(media)
        newmatrix.append(linha)
    
    return newmatrix, maxval

def medianmatrix(matrix,k,width,height): #monta a matrix com filtro de média k*k
    fator = int((k-1)/2) # define o fator de locomoção, número de linhas ou colunas queserão percorridas para cada "lado" do pixel central
    maxval = 0 #cria a variável que determinará o maxval
    newmatrix = [] #cria a matrix nova
    for indicelinha in range(height): #percorre todas as linhas da mterix
        linha = [] #cria a linha da matrix
        for indicecoluna in range(width): #percorre todas as colunas da mtrix
            
            #faz a soma dos valores numa região k*k
            valores = []
            for indlinha in range(indicelinha-fator,indicelinha+fator+1): 
                for indcoluna in range(indicecoluna-fator,indicecoluna+fator+1):
                    if 0 <= indlinha < height and 0 <= indcoluna < width: #evita o erro de indice nas bordas, como estamos utilizando zero padding, basta não contablizar valores além das bordas
                        valores.append(matrix[indlinha][indcoluna])
                    else:
                        valores.append(0)
            valores = sorted(valores)
            
            if int(len(valores)/2)*2 == len(valores): #calcula a mediana
                mediana = (valores[int(len(valores)/2)] + valores[int(len(valores)/2 - 1)])/2
            else:
                mediana = valores[int(len(valores)/2)]
                
            median = int(mediana) #pega a parte inteira da mediana
            
            if median > maxval:
                maxval = median
            linha.append(median)
        newmatrix.append(linha)
    
    return newmatrix, maxval

def mean(matrix,width,height):
    #calcula a soma dos valores da matrix
    soma = 0
    for linha in matrix:
        for value in linha:
            soma += value
            
    return int(soma/(width*height)) #retorna a média dos valores

def median(matrix):
    #cria uma lista com todos os valores
    listadamatrix = []
    for linha in matrix:
        for value in linha:
            listadamatrix.append(value)
            
    listadamatrix = sorted(listadamatrix)#ordena a lista
    
    #calcula a mediana
    if int(len(listadamatrix)/2)*2 == len(listadamatrix): 
        mediana = (listadamatrix[int(len(listadamatrix)/2)] + listadamatrix[int(len(listadamatrix)/2 - 1)])/2
    else:
        mediana = listadamatrix[int(len(listadamatrix)/2)]
                
    return int(mediana) #pega a parte inteira da mediana

def sobel(matrix1,matrix2,width,height):
    
    newmatrix = []
    maxval = 0
    
    #percorre as matrizes fazendo a raiz da soma dos quadrados do valor de cada matriz
    for linha in range(height):
        novalinha = []
        for coluna in range(width):
            value = hypot(matrix1[linha][coluna],matrix2[linha][coluna]) #calcula o valor
            if value > maxval:
                maxval = value
            novalinha.append(value) #salva o valor na linha
        newmatrix.append(novalinha) #salva a linha na matrix

    return newmatrix,maxval #retorna a matrix resultante

def kernel(matrix,lista,width,height):
    
    newmatrix = []
    
    #seleciona qual pixel será calculado
    for linha in range(height):
        novalinha = []
        for coluna in range(width):
            
            somatoria = 0
            indice = 0
            
            #seleciona qual será somado
            for slinha in range(linha-1,linha+2):
                for scoluna in range(coluna-1,coluna+2):
                    
                    if 0 <= slinha < height and 0 <= scoluna < width:
                        somatoria += matrix[slinha][scoluna]*lista[indice]
                    indice += 1
                    
            novalinha.append(somatoria)
        newmatrix.append(novalinha)
        
    return newmatrix
                    
def normalizacao(newmatrix,maxval,width,height):

    fator = 255/maxval
    
    for linha in range(height):
        for coluna in range(width):
            
            #faz o cálculo do valor equivalente para a escala 0 a 255
            value = newmatrix[linha][coluna]*fator
            
            #faz a aproximação para o inteiro mais próximo
            if abs(int(value) - value) >= 0.5:
                newmatrix[linha][coluna] = int(value) + 1
            else:
                newmatrix[linha][coluna] = int(value)

    return newmatrix

if __name__ == "__main__": #chama a função "geral" apenas se o .py não for importado
    geral()