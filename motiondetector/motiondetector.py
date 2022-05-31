###################################################################
# Nome do script    : motiondetector.py
# Sequência         : 4.2.2
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv
import numpy as np

# Inicializa um objeto VideoCapture
cap = cv.VideoCapture(0)

gray = cap.read()[1] # recebe o primeiro frame

# Verifica se a câmera está aberta
if cap.isOpened():
    ret, frame = cap.read()
    while ret:
        # ret: variável booleana. Retorna True se o frame é lido corretamente
        ret, frame = cap.read()

        gray_compare = gray # recebe o frame anterior
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # recebe o frame posterior

        # Separa os planos da imagem
        planes_compare = cv.split(gray_compare)
        planes = cv.split(gray)

        histSize = 64 # bins (segmentação do intervalo do histograma em subpartes)
        histRange = (0, 256) # intervalo do histograma
        accumulate = False
        
        # Calcula o histograma do plano da imagem (frame)
        hist_comp = cv.calcHist(planes_compare, [0], None, [histSize], histRange, accumulate=accumulate)
        hist = cv.calcHist(planes, [0], None, [histSize], histRange, accumulate=accumulate)

        hist_w = 640
        hist_h = 480
        bin_w = int(round(hist_w/histSize)) # largura do bin

        histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

        # Normaliza o histograma com base nos parâmetros indicados
        cv.normalize(hist_comp, hist_comp, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
        cv.normalize(hist, hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
        
        for i in range(1, histSize):
            cv.line(histImage, (bin_w*(i), hist_h - int(hist[i])),
                               (bin_w*(i), hist_h),
                               (255, 255, 255), thickness=2)

        # Comparação dos histogramas
        metric_val = cv.compareHist(hist_comp, hist, cv.HISTCMP_CORREL)
        if metric_val < 0.90:
            gray = cv.flip(gray, 1) # inverte a image horizontalmente
            cv.putText(gray, 'Movimento detectado!', (200, 400), cv.FONT_ITALIC, 1, (0, 255, 255), thickness=2)
            cv.imshow('Webcam', gray)
            cv.imshow('calcHist Demo', histImage)
        else:
            # Exibe a imagem capturada pela webcam
            cv.imshow('Webcam', cv.flip(gray, 1))
            # Exibe o histograma
            cv.imshow('calcHist Demo', histImage)
        if cv.waitKey(100) == ord('q'): # retorna um número inteiro representando o ponto de código Unicode desse caractere
            break

cap.release()
cv.destroyAllWindows()