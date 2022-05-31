###################################################################
# Nome do script    : trocaregioes.py
# Sequência         : 2.2.2
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv
import numpy as np

image = cv.imread('./trocaregioes/biel.png', 0)

h, w = image.shape
cX, cY = w // 2, h // 2

topLeft = image[0:cY, 0:cX]
topRight = image[0:cY, cX:w]
bottomLeft = image[cY:h, 0:cX]
bottomRight = image[cY:h, cX:w]

topImage = np.concatenate((topRight, topLeft), axis=1)
bottomImage = np.concatenate((bottomRight, bottomLeft), axis=1)
outputImage = np.concatenate((bottomImage, topImage), axis=0)

cv.imshow('Output image', outputImage)
cv.imwrite('./trocaregioes/biel-trocado.png', outputImage)
cv.waitKey(0)
cv.destroyAllWindows()