###################################################################
# Nome do script    : equalize.py
# Sequência         : 4.2.1
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Inicializa um objeto VideoCapture
cap = cv.VideoCapture(0)

# Verifica se a câmera está aberta
if cap.isOpened():
    ret, frame = cap.read()
    while ret:
        # ret: variável booleana. Retorna True se o frame é lido corretamente
        ret, frame = cap.read()

        # Separa os planos da imagem
        planes = cv.split(frame)

        histSize = 64 # bins (segmentação do intervalo do histograma em subpartes)
        histRange = (0, 256) # intervalo do histograma
        accumulate = False
        
        # Calcula o histograma para cada plano da imagem
        b_hist = cv.calcHist(planes, [0], None, [histSize], histRange, accumulate=accumulate)
        g_hist = cv.calcHist(planes, [1], None, [histSize], histRange, accumulate=accumulate)
        r_hist = cv.calcHist(planes, [2], None, [histSize], histRange, accumulate=accumulate)

        hist_w = 640
        hist_h = 480
        bin_w = int(round(hist_w/histSize)) # largura do bin

        histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

        # Normaliza o histograma com base nos parâmetros indicados
        cv.normalize(b_hist, b_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
        cv.normalize(g_hist, g_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
        cv.normalize(r_hist, r_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
        
        for i in range(1, histSize):
            cv.line(histImage, (bin_w*(i), hist_h - int(b_hist[i])),
                               (bin_w*(i), hist_h),
                               (255, 0, 0), thickness=2)
            cv.line(histImage, (bin_w*(i), hist_h - int(g_hist[i])),
                               (bin_w*(i), hist_h),
                               (0, 255, 0), thickness=2)
            cv.line(histImage, (bin_w*(i), hist_h - int(r_hist[i])),
                               (bin_w*(i), hist_h),
                               (0, 0, 255), thickness=2)


        # Exibe a imagem capturada pela webcam
        cv.imshow('Webcam', cv.flip(frame, 1))
        # Exibe o histograma
        cv.imshow('calcHist Demo', histImage)
        if cv.waitKey(100) == ord('q'): # retorna um número inteiro representando o ponto de código Unicode desse caractere
            break
    cv.imwrite('./equalize/histograma.png', histImage)
    cv.imwrite('./equalize/imagem-entrada.png', cv.flip(frame, 1))

cap.release()
cv.destroyAllWindows()