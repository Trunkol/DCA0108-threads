# Python program to illustrate the concept 
# of threading 
import threading, os, copy
from pprint import pprint
from pgm import pgmread, pgmwrite
import numpy as np

def alargamento_contraste(imagem): 
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name))

    nova_imagem = np.zeros((480, 640))

    for x in range(len(imagem[0])):
        for y in range(len(imagem[0][x])):
            nova_imagem[x][y] = imagem[0][x][y]

    pgmwrite(nova_imagem, 'teste.pgm')

def equalizacao_histograma(imagem): 
    print("Task 2 assigned to thread: {}".format(threading.current_thread().name)) 
  
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

    
