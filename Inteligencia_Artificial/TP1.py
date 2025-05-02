import numpy as np
from collections import deque
from PIL import Image

def binariza_imagem(caminho_imagem, limiar):

    imagem = Image.open(caminho_imagem).convert('L')#abre e converte a imagem para escala de cinza
    
    largura, altura = imagem.size
    pixels = imagem.load()
    
    matriz_binaria = []
    
    for y in range(altura):
        linha = []
        for x in range(largura):
            intensidade = pixels[x, y]#valores de 0 a 255
            if intensidade >= limiar:#se a intesidade for maior que o limiar vira 1, se for menor vira 0
                linha.append(1)
            else:
                linha.append(0)
        matriz_binaria.append(linha)
    
    return matriz_binaria

caminho = "imagem_binaria.png"#escrever o caminho para a imagem no computador

#matriz = binariza_imagem(caminho, limiar=128)#passa um numero para ser o limiar

matriz =  [
    [0,0,1,1,0,0,0,1,0,0],
    [0,0,1,1,0,0,0,1,0,0],
    [0,0,0,0,0,1,1,0,0,0],
    [1,1,0,0,0,1,1,0,0,0],
    [1,1,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,1,1],
    [0,1,0,0,1,0,0,0,0,0],
    [0,1,0,0,1,0,0,1,1,0],
    [0,0,0,0,0,0,0,1,1,0],
    [1,1,0,0,0,0,0,0,0,0],
]
#print(matriz)

contador = 1
linhas = len(matriz)#tamanho da imagem
colunas = len(matriz[0])#tamanho da imagem
rotulos = np.zeros((linhas,colunas), dtype=int)#usa numpy para criar uma matriz nula
vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]# define os vizinhos com conectividade 4 (cima,baixo,esquerda depois direita)

"""
implementando busca em largura porque é mais simples de implementar com a fila(deque) e pq facilita o 
entendimento do crescimento do rótulo. Dessa forma ele cresce em "ondas"
"""

def busca(x_inicial, y_inicial):
    fila = deque()#cria a fila (FIFO)
    fila.append((x_inicial, y_inicial))#começa a busca pelo primeiro pixel
    rotulos[x_inicial][y_inicial] = contador#o contador é o rótulo atual e conta quantos rótulos tem

    while fila:
        x, y = fila.popleft()#remove o primeiro item da fila para processar os vizinhos.



        for dx, dy in vizinhos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < linhas and 0 <= ny < colunas:
                if matriz[nx][ny] == 1 and rotulos[nx][ny] == 0:#se o vizinho é um pixel ativo e ainda não foi rotulado
                    rotulos[nx][ny] = contador#atribui o mesmo rótulo ao vizinho
                    fila.append((nx, ny))

for i in range(linhas):#percorre todos os pixels da imagem
    for j in range(colunas):
        if matriz[i][j] == 1 and rotulos[i][j] == 0:
            busca(i, j)
            contador += 1

print("Matriz de rótulos:")
for linha in rotulos:
    print(linha)

print(f"\nComponentes encontrados: {contador - 1}")