###################################################################
# Nome do script    : tiltshiftvideo.py
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

# Estabelece o gatilho para iniciar a gravação
record = False

# Inicializa um objeto VideoCapture
cap = cv.VideoCapture('./tiltshiftvideo/video.mp4')

if not cap.isOpened():
    print('Falha ao tentar abrir o vídeo.')

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Estabelece os parâmetros necessários para salvar o vídeo
out = cv.VideoWriter('./tiltshiftvideo/video-saida.avi', cv.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

# Variáveis para controle de velocidade
speed_controller = 6
speed_ratio = 0

while True:
    ret, frame = cap.read()
    # ret: variável booleana. Retorna True se o frame é lido corretamente
    if ret:
        # Verifica se o resto da divisão entre as variáveis é zero
        if speed_ratio % speed_controller == 0:
            # Recebe os valores da barra de rolagem
            l1 = cv.getTrackbarPos('l1', 'Controllers')
            l2 = cv.getTrackbarPos('l2', 'Controllers')
            d = cv.getTrackbarPos('d', 'Controllers')
            ksize = cv.getTrackbarPos('ksize', 'Controllers')

            # Aplica a função de ponderação
            l1 = add_weighted(x=l1, y=(frame.shape[0]))
            l2 = add_weighted(x=l2, y=(frame.shape[0]))
            l2 = l1 + l2

            # Recebe o resultado da aplicação da técnica de tilt shift
            img = tilt_shift(image=frame, l1=l1, l2=l2, d=d, ksize=ksize)

            # Exibe a imagem
            cv.imshow('Output Image', img)

            if cv.waitKey(1) == ord('r'):
                record = True

            if record:
                out.write(img)

            # Define a condição de parada: tecla "q"
            if cv.waitKey(1) == ord('q'):
                break

            # Incrementa a taxa de velocidade
            speed_ratio = speed_ratio + 1
        else:
            # Incrementa a taxa de velocidade
            speed_ratio = speed_ratio + 1
    else:
        # Reinicia o vídeo
        cap = cv.VideoCapture('./tiltshiftvideo/video.mp4')

cap.release()
out.release()
cv.destroyAllWindows()
