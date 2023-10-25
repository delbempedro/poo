import argparse

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
        
    def informacoes(self):
        return self._magicnumber,self._width,self._height,self._maxval,self._valores,self._median,self._mean,self._T
        
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
    
def geral(): #executa a totalidade do código
    try: #tenta executar o programa
        arquivo, metodo, argumento, savesite = leitura() #leitura do arquivo
        
        magicnumber,width,height,maxval,matrix = geramatrix(arquivo) #tratamento das informções do arquivo
        
        imagem = Image(magicnumber,width,height,maxval,matrix) #cria imagem com as informações tratadas
        
        if metodo == 'thresholding':
            Newimage = imagem.thresholding(argumento)
            
        elif metodo == 'sgt':
            Newimage = imagem.sgt(argumento)
            informacoes(Newimage,imagem,magicnumber,width,height,maxval) #faz o print das informações

            
        elif metodo == 'mean':
            Newimage = imagem.mean(argumento)
            
        else:
            Newimage = imagem.median(argumento)
            
        salvar(Newimage,arquivo,metodo,argumento,savesite)
        
    except ValueError: #se o parâmetro não corresponder ao método, apresenta a mensagem de erro
        print("O parâmetro fornecido não corresponde ao método fornecido, tente novamente!")
        
def leitura(): #faz a leitura da linha de comando
    parser = argparse.ArgumentParser(description = 'Leitura da linha de comando') #cria o objeto que será responsável por analisar os argumentos passados pelo terminal

    
    #salva os parâmetros
    #como funciona: pega '--something', faz 'action =' e salva em 'dest =' com valor default 'default =', 'required =' diz se o valor é obrigatório, 'help =' determina o que será impresso caso o usuário dê o comando '-h'
    parser.add_argument('--imgpath', action = 'store', dest = 'arquivo',
                        required = True, help = 'O arquivo que deseja-se tratar com o caminho até ele' )
    parser.add_argument('--op', action = 'store', dest = 'metodo',
                        required = True, help = 'O método a ser utilizado')
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

    #testa se os parâmetro corresponde ao método
    if (arguments.metodo == 'thresholding' and arguments.arg1 == None) or (arguments.metodo == 'sgt' and arguments.arg2 == None) or ( (arguments.metodo == 'mean' or arguments.metodo == 'median' )and arguments.arg3 == None):
        raise ValueError()
    else: #se o parâmetro corresponde ao método, salva 
        if arguments.metodo == 'thresholding':
            arg = int(arguments.arg1)
        elif arguments.metodo == 'sgt':
            arg = int(arguments.arg2)
        else:
            arg = int(arguments.arg3)
                
    return arguments.arquivo, arguments.metodo, arg, arguments.savesite


def salvar(image,arquivo,metodo,argumento,savesite):
    
    imagem = str(arquivo.split('/')[-1].split('.')[0]) #separa o nome do arquivi do diretório
    
    if metodo == 'thresholding':
        tipodoarg = 't'
    elif metodo == 'sgt':
        tipodoarg = 'dt'
    else:
        tipodoarg = 'k'
    
    nomedoarquivo = str( imagem + "_" + metodo + "_" + tipodoarg + str(argumento) )
    
    infos = image.informacoes() #pega as informacoes pertinentes para a escrita do arquivo
    
    if savesite: #verifica se savesite foi fornecido
        nomedoarquivo_ = savesite+'/'+nomedoarquivo+'.pgm'
    else:
        nomedoarquivo_ = nomedoarquivo+'.pgm'
     
    with open(nomedoarquivo_,'w', encoding='utf-8') as file:
        file.write(infos[0]+'\n') #escreve o número mágico
        file.write(str(infos[1])+' '+str(infos[2])+'\n') #escreve as dimensões do arquivo
        file.write(str(infos[3])+'\n') #escreve o maxval do arquivo
        
        for linha in infos[4]:
            for value in linha:
                file.write(str(value) +' ')
            file.write('\n')
    

def informacoes(Newimage,imagem,magicnumber,width,height,maxval):
    T = Newimage.informacoes()[-1][0]
    mean = imagem.informacoes()[-2]
    median = imagem.informacoes()[-3]
    print('magic_number',magicnumber)
    print('dimensions',(width,height))
    print('maxval',maxval)
    print('mean',mean)
    print('median',median)
    print('T',T)

def geramatrix(arquivo): #separa as informações do arquivo em magicnumber, widht, height, maxval e uma matrix com os valores dos pixels
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
        
        return magicnumber,width,height,maxval,matrix
    
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

if __name__ == "__main__": #chama a função "geral" apenas se o .py não for importado
    geral()