###################################################################
# Nome do script    : lapgauss.py
# Sequência         : 5.2
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv
import filters

cap = cv.VideoCapture(0)

if cap.isOpened():
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('Webcam', cv.flip(gray, 1))

        laplaciano = cv.filter2D(gray, -1, filters.laplacian)
        cv.imshow('Laplaciano', cv.flip(laplaciano, 1))

        gaussiano = cv.filter2D(gray, -1, filters.gauss)
        cv.imshow('Gaussiano', cv.flip(gaussiano, 1))

        laplacianoDoGaussiano = cv.filter2D(gaussiano, -1, filters.laplacian)
        cv.imshow('Laplaciano do gaussiano', cv.flip(laplacianoDoGaussiano, 1))

        # ord('q') retorna um número inteiro representando o ponto de código Unicode desse caractere
        if cv.waitKey(100) == ord('q'):
            break
    cv.imwrite('./laplgauss/webcam.png', cv.flip(gray, 1))
    cv.imwrite('./laplgauss/laplaciano.png', cv.flip(laplaciano, 1))
    cv.imwrite('./laplgauss/gaussiano.png', cv.flip(gaussiano, 1))
    cv.imwrite('./laplgauss/laplaciano-do-gaussiano.png', cv.flip(laplacianoDoGaussiano, 1))

cap.release()
cv.destroyAllWindows()