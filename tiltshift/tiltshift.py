###################################################################
# Nome do script    : tiltshift.py
# Sequência         : 6.2.1
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv
import numpy as np

# Para achar imagens para aplicar tilt shift, procurar por "images/videos taken by camera drone"

# l1 e l2 são as linhas cujo valor de alpha assume valor em torno de 0.5
# d  indica a força do decaimento da região
def tilt_shift(image, l1, l2, d, ksize=2):

    # Cria um vetor com as seguintes características:
    # start: 0
    # stop: image.shape[0] - 1
    # step: 1
    height = np.arange(image.shape[0], dtype=np.float32)

    if d == 0:
        alpha = (1/2)*(np.tanh((height - l1)/(1e-10)) -
                       np.tanh((height - l2)/(1e-10)))
    else:
        alpha = (1/2)*(np.tanh((height - l1)/(d)) - np.tanh((height - l2)/(d)))

    # Cria a máscara
    # Repete cada elemento n vezes, onde n é a quantidade de elementos contidos na dimensão de altura da imagem
    mask = np.repeat(alpha, image.shape[1])
    # Redimensiona a máscara para que ela tenha as mesmas dimensões da imagem
    # Cria uma máscara/matriz de colunas iguais a alpha
    mask = mask.reshape(image.shape[:2])

    # Verifica se a imagem está no sistema de cores RGB
    if len(image.shape) == 3:
        # Converte a cor da máscara
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

    # Define a máscara do filtro gaussiano
    kernel = (ksize * 2 + 1, ksize * 2 + 1)
    # Aplica o filtro gaussiano
    blur = cv.GaussianBlur(image, kernel, 0)

    # Retorna a imagem após a aplicação da técnica
    return cv.convertScaleAbs(image * mask + blur * (1 - mask))

# Função de ponderação
def add_weighted(x, y):
    return ((y * x)/100)

# Função de callback
def callback(x): return None

# Cria a janela onde estarão os controladores
cv.namedWindow('Controllers')

# Cria os controladores
cv.createTrackbar('l1', 'Controllers', 0, 100, callback)
cv.createTrackbar('l2',  'Controllers', 0, 100, callback)
cv.createTrackbar('d', 'Controllers', 0, 100, callback)
cv.createTrackbar('ksize', 'Controllers', 0, 100, callback)

while True:

    # Recebe a imagem de entrada
    input_img = cv.imread('./tiltshift/img6.jpg')
    # Redimensiona a imagem proporcionalmente através da função image_resize() do módulo resize
    input_img = resize.image_resize(input_img, height=600)

    # Recebe os valores da barra de rolagem
    l1 = cv.getTrackbarPos('l1', 'Controllers')
    l2 = cv.getTrackbarPos('l2', 'Controllers')
    d = cv.getTrackbarPos('d', 'Controllers')
    ksize = cv.getTrackbarPos('ksize', 'Controllers')

    # Aplica a função de ponderação
    l1 = add_weighted(x=l1, y=(input_img.shape[0]))
    l2 = add_weighted(x=l2, y=(input_img.shape[0]))
    # Cria a janela de foco
    l2 = l1 + l2

    # Aplica a técnica de tilt shift
    output_img = tilt_shift(image=input_img, l1=l1, l2=l2, d=d, ksize=ksize)
    # Exibe a imagem de saída
    cv.imshow('Output Image', output_img)
    if cv.waitKey(1) == ord('q'): # retorna um número inteiro representando o ponto de código Unicode desse caractere
        # Salva a imagem final
        cv.imwrite('./tiltshift/tilt-shifted.jpg', output_img)
        break

cv.destroyAllWindows()
