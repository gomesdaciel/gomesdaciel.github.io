import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as file:
    position_list = pickle.load(file) # Carregas as coordenadas de click armazenadas no arquivo

width, height = 107, 48 # Largura e altura de um retângulo

def checkParkingSpaces(image_processed):

    space_counter = 0 # Contador de vagas

    free_space = [] # Lista de vagas disponíveis

    for i, position in enumerate(position_list):
        x, y = position

        image_crop = image_processed[y: y + height, x: x + width] # Recorta a área das vagas
        # cv2.imshow(str(x*y), image_crop)
        count = cv2.countNonZero(image_crop) # Retorna o número de pixels diferentes de zero na matriz
        
        # Exibe a quantidade de pixels por vaga
        # cvzone.putTextRect(frame, str(count), (x + 5, y + height - 5)
        #                   ,scale=1, thickness=1, offset=0, colorR=(100, 100, 100))
        
        if count < 800: # Limiar de pixels para considerar a disponibilidade da vaga
            color = (0, 180, 0)
            thickness = 2
            space_counter = space_counter + 1
            free_space.append(str(i + 1)) # Armazena as vagas disponíveis
        else:
            color = (0, 0, 180)
            thickness = 1

        # Exibe os IDs das vagas
        cvzone.putTextRect(frame, str(i + 1), (x + 80, y + height - 5)
                    ,scale=1, thickness=1, offset=0, colorR=color)

        # Desenha os retângulos sobre as vagas em tempo real
        cv2.rectangle(frame, position, (position[0] + width, position[1] + height), color, thickness)

    # Exibe a quantidade de vagas disponíveis por quantidade de total de vagas
    cvzone.putTextRect(frame, f'Free: {str(space_counter)}/{len(position_list)}', (25, 60), scale=3
                      ,thickness=5, offset=20, colorR=(0, 180, 0))
    
    # Exibe os IDs das vagas disponíveis
    cvzone.putTextRect(frame, f'Free spaces: {free_space}', (360, 25), scale=1
                    ,thickness=1, offset=5, colorR=(0, 180, 0))

while True:

    # Garante a repetição do vídeo
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converte a imagem em preto e branco
    blur = cv2.GaussianBlur(gray, (3, 3), 1) # Aplica o filtro gaussiano para reduzir as transições abruptas
    # Aplica um threshold sobre a imagem borrada
    # cv2.adpativeThreshold determina o limiar para um pixel com base em uma pequena região ao seu redor.
    # Ele é útil em condições adversas de iluminação
    threshold_image = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C
                                           ,cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(threshold_image, 5) # Aplica o filtro da média para minimizar os ruídos sal e pimenta
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(median, kernel, iterations=1) # Dilata os pixels da região recortada

    checkParkingSpaces(dilate)

    cv2.imshow('Frame', frame)
    cv2.imshow('Gaussian blur', blur)
    cv2.imshow('Threshold image', threshold_image)
    cv2.imshow('Median blur', median) 
    if cv2.waitKey(10) == 27:
        cv2.imwrite('Gaussian blur.png', blur)
        cv2.imwrite('Threshold image.png', threshold_image)
        cv2.imwrite('Median blur.png', median) 
        break

cap.release()
cv2.destroyAllWindows()