import cv2
from math import pi
import numpy as np

img = r'C:\Users\User\Desktop\Imagens IC\FluidDeg 120C - 5 - 4x.png'
frame = cv2.imread(img)

diameters = []

if frame is None:
    print(f"Não foi possível carregar a imagem em {img}")
    exit()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (1, 1), 0)
contrast = cv2.convertScaleAbs(blurred, alpha=1, beta=1)
_, thresh = cv2.threshold(contrast, 150, 255, cv2.THRESH_BINARY)
blurred2 = cv2.GaussianBlur(thresh, (21, 21), 0)
_, thresh2 = cv2.threshold(blurred2, 150, 255, cv2.THRESH_BINARY)
#invert = cv2.bitwise_not(blurred2)
contours, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = [cnt for cnt in contours if cv2.arcLength(cnt, True) / pi > 9]

# Loop através dos contornos para calcular diâmetros e desenhar contornos
for contour in filtered_contours:
    perimeter = cv2.arcLength(contour, True)
    diameter = perimeter / pi
    diameters.append(diameter * 1.571285)  # Conversão 1 px = 1.571285 um (obtido de 'calibrar.py')
    cv2.drawContours(frame, filtered_contours, -1, (0, 0, 255), 2)

while True:
    cv2.imshow('Bolhas detectadas', frame)
    keypress = cv2.waitKey(1)
    if keypress == ord('q'):
        break

# Calcular o diâmetro médio das bolhas
if diameters:
    mean_diameter = np.mean(diameters)
    for x in range(len(diameters)):
        print(diameters[x])
    print(f"Número de bolhas = {len(diameters)}\n"
          f"Diâmetro médio das bolhas: {mean_diameter:.2f} um")

else:
    print("Nenhuma bolha detectada.")

cv2.destroyAllWindows()