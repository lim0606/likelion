import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

#img = cv2.imread('faces.jpg')
img = cv2.imread('Aishwarya-Rai-face.jpg')

faces = face_cascade.detectMultiScale(img, 1.2, 5)
eyes = eye_cascade.detectMultiScale(img, 1.2, 5)

#print faces

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

for (x, y, w, h) in eyes:
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
