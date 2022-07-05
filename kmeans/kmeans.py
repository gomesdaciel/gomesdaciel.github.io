import cv2 as cv
import numpy as np

def kmeans(img):
    nClusters = 8
    nRodadas = 1
    
    altura = img.shape[0]
    largura = img.shape[1]
    
    amostras = img.reshape((-1,3))
    amostras = np.float32(amostras)
    
    compacidade, rotulos, centros = cv.kmeans(amostras,
                                    nClusters,
                                    None,
                                    (cv.TERM_CRITERIA_MAX_ITER | cv.TERM_CRITERIA_EPS, 10000, 0.0001),
                                    nRodadas,
                                    cv.KMEANS_RANDOM_CENTERS)

    centros = np.uint8(centros)
    resultado = centros[rotulos.flatten()]
    resultado = resultado.reshape(img.shape)

    return resultado

def main():
    img = cv.imread('cupcakes.jpg', cv.IMREAD_COLOR)

    for a in range(1, 10):
        rodada = kmeans(img)
        cv.imshow(f'Rodada {a}', rodada)


    cv.waitKey()
    cv.destroyAllWindows()
    
if __name__ == '__main__':
    main()