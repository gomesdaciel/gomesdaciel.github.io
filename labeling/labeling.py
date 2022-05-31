###################################################################
# Nome do script    : labeling.py
# Sequência         : 3.2
# Autores       	: Daciel Gomes e Marcelo Augusto
###################################################################

import cv2 as cv

img = cv.imread('./labeling/bolhas.png', cv.IMREAD_GRAYSCALE)

py, px = img.shape[:2]

# Retirando as bolhas que tocam as bordas
for y in range(py):
    for x in range(px):
        if (y == 0 or x == 0 or y == (py - 1) or x == (px - 1)) and img[y, x] == 255:
            cv.floodFill(img, None, (x, y), 0) 
            # Parâmetros do método cv2.floodFill: imagem, máscara (None), (altura, largura), cor (0 a 255)

cv.imwrite('./labeling/sem-bolhas-de-borda.png', img)

# Pintando as demais bolhas com tons de cinza
k = 0
for y in range(py):
    for x in range(px):
        if img[y, x] == 255:
            k = k + 1 # Propositalmente posicionado antes do método cv2.floodFill para que a bolha não seja
                      # preenchida com a cor preta (k = 0)
            cv.floodFill(img, None, (x, y), k)

cv.imwrite('./labeling/com-bolhas-pintadas.png', img)

# Pintando o exterior das bolhas com a cor branca
cv.floodFill(img, None, (0, 0), 255)

cv.imwrite('./labeling/com-exterior-pintado-de-branco.png', img)

numBolhas = 0
for y in range(py):
    for x in range(px):
        if img[y, x] == 0: # Procura pelos buracos (preenchidos com a cor preta)
            cv.floodFill(img, None, (x, y), 255)
            numBolhas = numBolhas + 1 # A variável numBolhas é incrementada sempre que o ocorre o "flood fill",
                                      # isto é, sempre que uma bolha com buraco é encontrada

cv.imwrite('./labeling/com-interior-pintado-de-branco.png', img)

print(f'Número bolhas: {k}\nNúmero de bolhas com buracos: {numBolhas}')

cv.imshow('bolhas', img)
cv.waitKey(0)
cv.destroyAllWindows()