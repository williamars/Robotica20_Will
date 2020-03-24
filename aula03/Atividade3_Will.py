import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def return_center(coefang1, coefang2, coeflinear1, coeflinear2):
    if coefang2 == coefang1:
        coefang2 = coefang1 + 1 
    
    # Calcula o ponto de fuga
    x_fuga = (-(coeflinear2 - coeflinear1)/(coefang2-coefang1))
    y_fuga = coefang1*x_fuga + coeflinear1
    
    # Retorna o ponto de fuga
    return (x_fuga, y_fuga)

# Fazendo a leitura do video
cap = cv2.VideoCapture('video1.mp4')

while(True):
    # Capturar Frame por Frame
    ret, frame = cap.read()
    
    # Caso apresente erro na captura
    if ret == False:
        print("Problema para capturar o frame!")

    # Mudando os tipos de captura de cor
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Fazendo a mascara para pegar a linha
    p_mask1 = np.array([240])
    p_mask2 = np.array([255])
    mascara = cv2.inRange(gray, p_mask1, p_mask2)
    
    blur = cv2.blur(mascara, (3,3))
    
    hough_img_rgb2 = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)
    min_contrast = 100
    max_contrast = 200
    linhas = cv2.Canny(hough_img_rgb2, min_contrast, max_contrast)
    
    # cv2.imshow('Canny', linhas)
    
    # Capturando linhas
    lines = cv2.HoughLinesP(linhas, 10, math.pi/180.0, 200, np.array([]), 5, 5)
    a,b,c = lines.shape
    hough_img_rgb = cv2.cvtColor(linhas, cv2.COLOR_GRAY2BGR)

    coeficientes_angulares = []
    coeficientes_lineares = []
    
    for i in range(a):
        # Linha ligando o ponto inicial ao ponto final
        #cv2.line(hough_img_rgb, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 5, cv2.LINE_AA)

        coef_agora = (lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0])
        coeficientes_angulares.append(coef_agora)
        coeficientes_lineares.append(lines[i][0][1] - (coef_agora*lines[i][0][0]))

        
        
    menor_coef_angular = min(coeficientes_angulares)
    maior_coef_angular = max(coeficientes_angulares)
    indice_menor = coeficientes_angulares.index(menor_coef_angular)
    indice_maior = coeficientes_angulares.index(maior_coef_angular)
    
    maior_linear = coeficientes_lineares[indice_maior]
    menor_linear = coeficientes_lineares[indice_menor]
    
    # Pegando o ponto de fuga
    fuga = return_center(maior_coef_angular, menor_coef_angular, maior_linear, menor_linear)
    
    # Circulo
    cv2.circle(hough_img_rgb, (int(fuga[0]), int(fuga[1])), 20, (233,20,255))
    # Centro do circulo
    cv2.circle(hough_img_rgb,(int(fuga[0]),int(fuga[1])),5,(255,140,255),3)
    
    cv2.line(hough_img_rgb, (lines[i][0][0], lines[i][0][1]), (int(fuga[0]),int(fuga[1])), (0,0,255), 5)
    
    cv2.imshow('hough', hough_img_rgb)
   
    # Se apertar 'q', o programa fecha
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura, quando tudo estiver pronto
cap.release()
cv2.destroyAllWindows()