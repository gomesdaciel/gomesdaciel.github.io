import cv2
import pickle

image = cv2.imread('carParkImg.png')

# Largura e altura dos retângulos sobre as vagas
width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as file:
        position_list = pickle.load(file) # Carregas as coordenadas de click armazenadas no arquivo
except:
    position_list = []

# Define a função callback para eventos do mouse
def mouse_click(events, x, y, flags, parameters):
    if events == cv2.EVENT_LBUTTONDOWN:
        position_list.append((x, y)) # Armazena as coordenadas do click
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(position_list):
            x1, y1 = position
            if (x1 < x < (x1 + width)) and (y1 < y < (y1 + height)):
                position_list.pop(i) # Remove as coordenadas do click se o evento ocorrer dentro da área específicada
    
    with open('CarParkPos', 'wb') as file:
        pickle.dump(position_list, file) # Armazena as coordenadas do click mesmo após a finalização do script


while True:
    image = cv2.imread('carParkImg.png')

    for position in position_list:
        # Desenha os retângulos sobre as vagas
        cv2.rectangle(image, position, (position[0] + width, position[1] + height), (255, 0, 255), 2)

    cv2.imshow('Image', image)
    cv2.setMouseCallback('Image', mouse_click)
    if cv2.waitKey(1) == 27:
        cv2.imwrite('EditedImage.png', image)
        break

cv2.destroyAllWindows()