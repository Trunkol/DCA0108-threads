# Python program to illustrate the concept 
# of threading 
import threading, os, copy
from pprint import pprint
from pgm import pgmread, pgmwrite
import numpy as np

def __extrair_imax(imagem):
    return int(imagem[0].astype(np.float).max())

def __extrair_imin(imagem):
    return int(imagem[0].astype(np.float).min())

def alargamento_contraste(imagem): 
    print("Executando a thread: {}".format(threading.current_thread().name))
    nova_imagem = np.zeros((480, 640))
    imax = __extrair_imax(imagem)
    imin = __extrair_imin(imagem)
    for x in range(len(imagem[0])):
        for y in range(len(imagem[0][x])):
            processamento = (255/(imax - imin)) * (imagem[0][x][y].astype(np.int) - imin)
            nova_imagem[x][y] = round(processamento)

    pgmwrite(nova_imagem, 'alargamento_final.pgm')

def __calcular_histograma(imagem):
    h = np.zeros(256)
    for x in range(len(imagem[0])):
        for y in range(len(imagem[0][x])):
            h[imagem[0][x][y].astype(np.int)] += 1
    return h

def __calcular_probabilidade_ocorrencia(h):
    p = np.zeros(256)
    for i in range(256):
        p[i] = h[i] / (480 * 640)
    return p

def __calcular_probabilidade_acumulada(p):
    q = np.zeros(256)
    for i in range(256):
        cont = 0
        for j in range(i):
            cont = cont + p[j]
        q[i] = cont
    
    return q
    
def equalizacao_histograma(imagem): 
    print("Executando a thread: {}".format(threading.current_thread().name))
    h = __calcular_histograma(imagem)
    p = __calcular_probabilidade_ocorrencia(h)
    q = __calcular_probabilidade_acumulada(p)
    
    nova_imagem = np.zeros((480, 640))
    for x in range(len(imagem[0])):
        for y in range(len(imagem[0][x])):
            nova_imagem[x][y] = round(255* q[imagem[0][x][y].astype(np.int)])
    
    pgmwrite(nova_imagem, 'equalizacao_histograma.pgm')
    
if __name__ == "__main__": 
    img_original = pgmread('balloons.ascii.pgm')    
    # deepcopy para evitar condição de corrida
    img_tratamento_1 = copy.deepcopy(img_original)
    img_tratamento_2 = copy.deepcopy(img_original)
    
    # criando threads
    t1 = threading.Thread(target=alargamento_contraste, name='alargamento', args=(img_tratamento_1,)) 
    t2 = threading.Thread(target=equalizacao_histograma, name='equalização', args=(img_tratamento_2,))   

    # inicio das execuções
    t1.start() 
    t2.start() 
  
    # esperando até o final da execução
    t1.join() 
    t2.join() 

    
 