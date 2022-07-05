import cv2 as cv
import numpy as np


def callback(x): pass


def pointilhismo(img):
    altura = img.shape[0]
    largura = img.shape[1]
    point = np.zeros(img.shape, dtype=np.uint8)
    STEP = 5
    RAIO = 3
    JITTER = 3

    xrange = np.arange(0, altura-STEP, STEP) + STEP // 2
    yrange = np.arange(0, largura-STEP, STEP) + STEP // 2

    np.random.shuffle(xrange)
    for i in xrange:
        np.random.shuffle(yrange)
        for j in yrange:
            x = i + np.random.randint((2 * JITTER) - JITTER + 1)
            y = j + np.random.randint((2 * JITTER) - JITTER + 1)
            cor = img[x, y]
            point = cv.circle(point, (y, x), RAIO, (int(cor[0]), int(
                cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)
    cv.imshow('POINTILHISMO', point)
    return point


def pointilhismo_canny(img, pointilhismo, t):
    result = pointilhismo.copy()

    for i in range(0, 6, 1):
        canny = cv.Canny(img, i*t, i*t*3)
        pontos = np.where(canny != 0)
        pontos = zip(pontos[0], pontos[1])
        for p in pontos:
            cor = img[p]
            result = cv.circle(result, (p[1], p[0]), i,  (int(cor[0]), int(
                cor[1]), int(cor[2])), -1, lineType=cv.LINE_AA)
    return result


def main():
    img = cv.imread('uvas.jpg')
    cv.imshow('ORIGINAL', img)
    cv.namedWindow('POINTILHISMO')
    cv.namedWindow('CANNY')
    cv.namedWindow('POINTILHISMO AJUSTADO')
    cv.createTrackbar('T', 'CANNY', 20, 255, callback)

    while True:
        t = cv.getTrackbarPos('T', 'CANNY')
        canny = cv.Canny(img, t, t*3)
        cv.imshow('CANNY', canny)
        resultado = pointilhismo_canny(img, pointilhismo(img), t)
        cv.imshow('POINTILHISMO AJUSTADO', resultado)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
