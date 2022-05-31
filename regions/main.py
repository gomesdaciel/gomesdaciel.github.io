###################################################################
# Nome do script    : regions.py
# Sequência         : 2.2.1
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv

def regions(image, x0, y0, x1, y1):
    for x in range(min(x0, x1), max(x0, x1)):
        for y in range(min(y0, y1), max(y0, y1)):
            image[x, y] = 255 - image[x, y]
    return image

x0, y0 = map(int, input('Informe as coordenadas (X, Y) do ponto P1: ').split())
x1, y1 = map(int, input('Informe as coordenadas (X, Y) do ponto P2: ').split())

img = regions(image=cv.imread('./regions/biel.png', cv.IMREAD_GRAYSCALE), x0=x0, y0=y0, x1=x1, y1=y1)

cv.imshow('Output image', img)
cv.waitKey(0)
cv.imwrite('./regions/biel-negativo.png', img)
cv.destroyAllWindows()
