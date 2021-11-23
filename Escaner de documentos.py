import cv2
import numpy as np
from PIL import Image
import os



def ordenar_a(a):
	x = np.concatenate([a[0], a[1], a[2], a[3]]).tolist()

	eje_y = sorted(x, key=lambda x: x[1])

	eje_x = eje_y[:2]
	eje_x = sorted(eje_x, key=lambda eje_x: eje_x[0])

	eje_x2 = eje_y[2:4]
	eje_x2 = sorted(eje_x2, key=lambda eje_x2: eje_x2[0])
	
	return [eje_x[0], eje_x[1], eje_x2[0], eje_x2[1]]
	
image = cv2.imread('img0.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 10, 150)

cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

for c in cnts:
	epsilon = 0.01*cv2.arcLength(c,True)
	approx = cv2.approxPolyDP(c,epsilon,True)
	
	if len(approx)==4:
		cv2.drawContours(image, [approx], 0, (0,255,255),2)
		
		a = ordenar_a(approx)

		cv2.circle(image, tuple(a[0]), 7, (255,0,0), 2)
		cv2.circle(image, tuple(a[1]), 7, (0,255,0), 2)
		cv2.circle(image, tuple(a[2]), 7, (0,0,255), 2)
		cv2.circle(image, tuple(a[3]), 7, (255,255,0), 2)
		
		pts1 = np.float32(a)
		pts2 = np.float32([[0,0],[270,0],[0,310],[270,310]])
		M = cv2.getPerspectiveTransform(pts1,pts2)
		dst = cv2.warpPerspective(gray,M,(270,310))
		
		

filtro = cv2.GaussianBlur(dst, (0,0), 3)
filtro = cv2.addWeighted(dst, 1.5, filtro, -0.5, 0)
filtro2 = cv2.adaptiveThreshold(filtro, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 15)
cv2.imshow('filtro2', filtro2)


cv2.imwrite('imagen.jpg',filtro2)

path = 'C:/Users/santi/OneDrive/Documentos/pythom/imagen.jpg'
pdf= Image.open(path)
pdf.save('C:/Users/santi/OneDrive/Documentos/pythom/escaner.pdf')
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
