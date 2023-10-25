from math import hypot
import sys

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
    
    
    def thresholding(self,t=127):
        #aplica thresholding
        self._T = t
        newmatrix = thres(self._valores,self._T)

        return Image(self._magicnumber,self._width,self._height,255,newmatrix)
    
    def sgt(self,dt=1):
        
        med = media(self._valores,self._width,self._height) #calcula o valor médio dos pixels
        newt = med #salva a média como novo parâmtro para o thresholding
        oldt = 127 #valor arbitrário, escolhido apenas para definir o oldt de modo que o loop a seguir funcione

        while dt < abs(newt-oldt): #calcula um novo t até que a diferença entre oldt e newt seja menor que dt
            
            oldt = int(newt) #salva o valor de t atual, em oldt, antes de alterá-lo
            newt = calcularnovot(self._valores,oldt) #calcula um novo valor para o parâmetro t
        
        nmatrix = thres(self._valores,newt)
        
        self._T = int(newt)
        
        return Image(self._magicnumber,self._width,self._height,255,nmatrix,self._T)
            
    def mean(self,k=3):
        
        newmatrix,maxval = meanmatrix(self._valores,k,self._width,self._height)

        return Image(self._magicnumber,self._width,self._height,maxval,newmatrix)
        
    def median(self,k=3):
        
        newmatrix,maxval = medianmatrix(self._valores,k,self._width,self._height)
        
        return Image(self._magicnumber,self._width,self._height,maxval,newmatrix)

    def sobel(self):
        
        #calcula os kernels
        matrix1 = kernel(self._valores,[1,0,-1,2,0,-2,1,0,-1],self._width,self._height)
        matrix2 = kernel(self._valores,[1,2,1,0,0,0,-1,-2,-1],self._width,self._height)
        
        #calcula a "hipotenusa" entre os pontos dos kernels
        newmatrix,maxval = sobel(matrix1,matrix2,self._width,self._height)
        
        #"normaliza" os valores para uma escala de 0 a 255
        newmatrix = normalizacao(newmatrix,maxval,self._width,self._height)
    
        return Image(self._magicnumber,self._width,self._height,255,newmatrix)

    
def geral(): #executa a totalidade do código
    try: #tenta executar o programa
        arquivo, metodos, argumentos, savesite = leitura() #leitura do arquivo
        
        oldimagem = leimagem(arquivo) #cria imagem com as informações tratadas
        imagem = oldimagem
        
        #executa as operações desejadas na sequência fornecida
        contador = 0
        metargs = []
        for metodo in metodos:
            
            #verifica se o método é compátível com o argumento
            if contador < len(argumentos):
                argcompativel(metodo,argumentos[contador]) 

            if metodo == 'thresholding':
                imagem = imagem.thresholding(int(argumentos[contador+1]))
                metargs.append([metodo,argumentos[contador+1]]) #salva qual metodo foi utlizado com qual argumento
                
            elif metodo == 'sgt':
                imagem = imagem.sgt(int(argumentos[contador+1]))
                metargs.append([metodo,argumentos[contador+1]]) #salva qual metodo foi utlizado com qual argumento
            
            elif metodo == 'sobel':
                imagem = imagem.sobel()
                metargs.append(metodo) #salva qual metodo foi utlizado com qual argumento
                
            elif metodo == 'mean':
                imagem = imagem.mean(int(argumentos[contador+1]))
                metargs.append([metodo,argumentos[contador+1]]) #salva qual metodo foi utlizado com qual argumento
                
            else:
                imagem = imagem.median(int(argumentos[contador+1]))
                metargs.append([metodo,argumentos[contador+1]]) #salva qual metodo foi utlizado com qual argumento
                
            if metodo != 'sobel': #pula os parâmetros já utilizados (exemplo: [...,--dt,4,...] são pulados)
                contador += 2
                
        if 'sgt' in metodos: #faz o print das informações caso sgt seja um dos métodos chamados
            printinformacoes(imagem,oldimagem)
        
        salvar(imagem,arquivo,metargs,savesite)
        
    except ArgumentoInvalido: #se o parâmetro não corresponder ao método, apresenta a mensagem de erro
        print("O parâmetro fornecido não corresponde ao método fornecido, tente novamente!")

def leitura(): #faz a leitura da linha de comando
    infos = sys.argv #salva as informções da linha de comando

    #salva as informações de onde o arquivo deve ser salvo
    if '--outputpath' == infos[-2]:
        savesite = infos.pop(-1)
        del(infos[-1])
    else:
        savesite = None
    
    for indice in range(len(infos)): #percorre os indices de infos
        
        if infos[indice] == '--imgpath': #salva o endereço da imagem a ser utilizada
            arquivo = infos[indice + 1]
            
        if infos[indice] == '--op': #salva os métodos a serem utilizados
            arguments = []

            for value in range(indice+1,len(infos)):
                if value != '--outputpath':
                    arguments.append(infos[value])

            auxiliar = tratametodos(arguments)
            metodos, args = auxiliar[0], auxiliar[1]
    
    return arquivo, metodos, args, savesite       

class ArgumentoInvalido(ValueError): #cria um tipo de erro específico para não confundir com erros de códigos
    pass

def tratametodos(lista): #separa as informações de --op em metodos e argumentos
    metodos = []
    args = []

    for item in lista:
        
        #"limpa" o items
        realitem = None
        for caracter in item:
            if caracter != '[' and caracter != ']' and caracter != '':
                if not realitem:
                    realitem = caracter
                else:
                    realitem += caracter

        #separa os items em métodos e argumentos
        if realitem == 'thresholding' or realitem == 'sgt' or realitem == 'mean' or realitem == 'median' or realitem == 'sobel':
            metodos.append(realitem)
        else:
            args.append(realitem)
            
    return metodos, args

def salvar(image,arquivo,metargs,savesite):
    
    imagem = str(arquivo.split('/')[-1].split('.')[0]) #separa o nome do arquivo do diretório
    
    nomedoarquivo = str(imagem)
    for tupla in metargs:
        if len(tupla) == 2:
            nomedoarquivo = nomedoarquivo + "-" + str(tupla[0]) + "-" + str(tupla[1])
        else:
            nomedoarquivo = nomedoarquivo + "-" + str(tupla)
    
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
    
    return (1/2)*(m1+m2) #retorna o newt

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
    
    for linha in range(height):
        for coluna in range(width):
            
            newmatrix[linha][coluna] = round(255 * newmatrix[linha][coluna]/ maxval)

    return newmatrix

def argcompativel(metodo,arg): #verifica se o argumento é compatível com método
    if (metodo == 'thresholding' and arg != '--t') or (metodo == 'sgt' and arg != '--dt') or (metodo == 'median' and arg != '--k') or (metodo == 'median' and arg != '--k'):
        raise ArgumentoInvalido()
    
def cadeOerro(matriz1,matriz2,width,height):
    for i in range(height):
        for j in range(width):
            if matriz1[i][j] != matriz2[i][j]:
                print("ME DESCULPE!!!, eu falhei na linha",i,"coluna",j,"eu deveria ser",matriz2[i][j],"mas sou",matriz1[i][j])

if __name__ == "__main__": #chama a função "geral" apenas se o .py não for importado
    geral()