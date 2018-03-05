
#INICIO DE OPENCV PARA DETECCION FACIAL
import cv2 #Libreria de opencv
i=0
#cargamos la plantilla e inicializamos la webcam:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while(True):
   #leemos un frame y lo guardamos
   ret, img = cap.read()

   #convertimos la imagen a blanco y negro
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   #buscamos las coordenadas de los rostros (si los hay) y
   #guardamos su posicion
   faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
   #Dibujamos un rectangulo en las coordenadas de cada rostro
   for (x,y,w,h) in faces:
       cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)       
       break
   
   #Mostramos la imagen
   cv2.imshow('img',img)   
   
   #con la tecla 'q' salimos del programa
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

   i+=1   
   if i>5: #esperamos a que se estabilice la imagen para guardar una fotografia
      cv2.imwrite('save.jpg', img)
      break
   #detenemos el bucle para buscar caras
   #break

cap.release()
cv2.destroyAllWindows()


#INICIO DE FBRECOG PARA RECONOCIMIENTO FACIAL
#Para dibujar rectangulos y nombres sobre las caras
from PIL import Image, ImageDraw, ImageFont

#Insert your access token obtained from Graph API explorer here
TOKEN='xxxx' 

# Insert your cookie string here
COOKIE='xxxx'

# Insert the fb_dtsg parameter obtained from Form Data here.
FB_DTSG='xxxx'

# Insert your image file path here    
photo='save.jpg'

#Open the image
img=Image.open(photo)

#Pasamos la imagen a dibujo para operar sobre ella
draw=ImageDraw.Draw(img)

#Configuramos los parametros de la fuente para poner el nombre de cada cara
#ImageFont.truetype(FUENTE,TAMAÑO) 
font=ImageFont.truetype('arial.ttf',20)

w,h=img.size #Obtenemos las dimensiones de la foto para despues redimensionar las medidas obtenidas del wrapper

#An unofficial python wrapper for the Facebook face recognition endpoint
from fbrecog import FBRecog
    
# Instantiate the recog class
recog = FBRecog(TOKEN, COOKIE, FB_DTSG)

# Recog class can be used multiple times with different paths
#print(recog.recognize(photo))    

#print('-'*40)
# Call recognize_raw to get more info about the faces detected, including their positions
#print(recog.recognize_raw(photo))

# Call recognize_raw to get info about the positions of the face for draw an square
faces = recog.recognize_raw(photo)

# Recorremos todas las caras reconocidas
for face in faces:
    #Obtenemos las caracteriticas de cada reconocimiento
    name=face['recognitions']

    if name:
        #Imprime el nombre de usuario del rostro detectado
        #print('name: '+name[0]['user']['name'])
        
        #La foto que se sube a fb tiene un tamaño de 100x100 (miniatura), por lo tanto,
        #las coordenadas del centro de los rostros detectados estan de acuerdo a esa resolucion.
        #La foto original tiene una medida variable, las coordenadas originales no encajarian con 
        #las obtenidas de FB, para ajustar esto se propone
        #una sencilla regla de 3 para reescalar las coordenadas.

        #Se calcula la nueva posicion de la coordenada x con la medida del largo de la imagen original (w)
        posx=face['x']*w/100

        #Se calcula la nueva posicion de la coordenada y con la medida del alto de la imagen original (h)
        posy=face['y']*h/100

        #Dibujamos sobre la imagen un texto con el nombre de usuario
        #draw.text((coordenada_en_x,coordenada_en_y),texto,fill=color_del_texto,font=fuente_de_la_letra)
        draw.text((posx,posy),name[0]['user']['name'],fill='blue',font=font)

        #Para dibujar un rectangulo sobre el rostro tambien hay que escalar las medidas del alto y ancho del rostro detectado
        #(face['width']*w/100) y (face['height']*h/100)
        
        #Dibujamos un rectangulo sobre el rostro        
        #draw.rectangle(((posx+(face['width']*w/100)/2,posy+(face['height']*h/100)/2),(posx-(face['width']*w/100)/2,posy-(face['height']*w/100)/2)),fill=None,outline='red')
    else:
         draw.text((0,0),"No se encontraron rostros conocidos",fill='blue',font=40)

img.save('reconocidos.jpg')
