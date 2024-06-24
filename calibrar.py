import cv2
from math import pi
import numpy as np

img = r'C:\Users\User\Desktop\Imagens IC\Calibracao 40x 12-04 70um.png'
frame = cv2.imread(img)

diameters = []

if frame is None:
    print(f"Não foi possível carregar a imagem em {img}")
    exit()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 0)
# contrast = cv2.convertScaleAbs(blurred, alpha=0.4, beta=0)
_, thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY) #4x, 10x: 120,255 <---> 40x: 80,255
# blurred2 = cv2.GaussianBlur(thresh, (13, 13), 0)
invert = cv2.bitwise_not(thresh)
contours, _ = cv2.findContours(invert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = [cnt for cnt in contours if cv2.arcLength(cnt, True) / pi > 50]

# Loop através dos contornos para calcular diâmetros e desenhar contornos
for contour in filtered_contours:
    perimeter = cv2.arcLength(contour, True)
    diameter = perimeter / pi
    diameters.append(diameter)  # Armazenar o diâmetro individual da bolha
    cv2.drawContours(frame, filtered_contours, -1, (0, 0, 255), 2)

while True:
    cv2.imshow('Bolhas detectadas', frame)
    keypress = cv2.waitKey(1)
    if keypress == ord('q'):
        break

# Calcular o diâmetro médio das bolhas
if diameters:
    mean_diameter = np.mean(diameters)
    print(f"Número de bolhas = {len(diameters)}\nDiâmetro médio das bolhas: {mean_diameter:.2f} px")
    convert = 70 / mean_diameter #70 ou 600 um dependendo da calibração
    print(f"Fator de conversão = {convert:.6f} um / px")
else:
    print("Nenhuma bolha detectada.")

cv2.destroyAllWindows()