from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

#INICIO DE OPENCV PARA DETECCION FACIAL
import cv2 #Libreria de opencv
import time
i=0
flag=True

#cargamos la plantilla e inicializamos la webcam:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while(flag):
   #Espera un segundo antes de comenzar un nuevo ciclo
   time.sleep(1)

   #Si no es el procesador principal
   if rank!=0:
      #Cerramos cualquier actividad de la camara
      cap.release()
      cv2.destroyAllWindows()

      #Espera antes de tomar la siguiente captura de frames
      time.sleep(0.5*rank)
      cap = cv2.VideoCapture(0)
         
   #leemos un frame y lo guardamos
   ret, img = cap.read()

   #convertimos la imagen a blanco y negro
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   #buscamos las coordenadas de los rostros (si los hay) y
   #guardamos su posicion
   faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
   #Dibujamos un rectangulo en las coordenadas de cada rostro
   for (x,y,w,h) in faces:
       i+=1
       cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
       #detenemos el bucle cuando encuentra una cara
       flag=False
       break
   
   #Mostramos la imagen
   #cv2.imshow('img',img)   
   
   #con la tecla 'q' salimos del programa
   #if cv2.waitKey(1) & 0xFF == ord('q'):
   #    break
   
   #esperamos a que se estabilice o aparezca una cara visible en la imagen para guardar una fotografia      
   cv2.imwrite('save'+str(rank)+'.jpg', img)       

#Cerramos la camara
cap.release()
cv2.destroyAllWindows()

#INICIO DE FBRECOG PARA RECONOCIMIENTO FACIAL
#An unofficial python wrapper for the Facebook face recognition endpoint
from fbrecog import FBRecog

#Clase con los datos para el wrapper de FB
from credentials import credentials

#Para dibujar rectangulos y nombres sobre las caras
from PIL import Image, ImageDraw, ImageFont

#Insert your access token obtained from Graph API explorer here
TOKEN=credentials.Token

# Insert your cookie string here
COOKIE=credentials.Cookie

# Insert the fb_dtsg parameter obtained from Form Data here.
FB_DTSG=credentials.Fb_dstg

# Insert your image file path here    
photo='save'+str(rank)+'.jpg'

#Open the image
img=Image.open(photo)

#Pasamos la imagen a dibujo para operar sobre ella
draw=ImageDraw.Draw(img)

#Configuramos los parametros de la fuente para poner el nombre de cada cara
#ImageFont.truetype(FUENTE,TAMAÑO) 
font=ImageFont.truetype('arial.ttf',20)

#Obtenemos las dimensiones de la foto para despues redimensionar las medidas obtenidas del wrapper
w,h=img.size 
    
# Instantiate the recog class
recog = FBRecog(TOKEN, COOKIE, FB_DTSG)

# Recog class can be used multiple times with different paths
#print(recog.recognize(photo))    

#print('-'*40)
# Call recognize_raw to get more info about the faces detected, including their positions
#print(recog.recognize_raw(photo))

# Call recognize_raw to get info about the positions of the face for draw an square
faces = recog.recognize_raw(photo)

#Lista para agregar nombres de las personas reconocidas
users=[]
try:

   for face in faces:
       #Obtenemos las caracteriticas de cada reconocimiento
       name=face['recognitions']       

       #La foto que se sube a fb tiene un tamaño de 100x100 (miniatura), por lo tanto,
       #las coordenadas del centro de los rostros detectados estan de acuerdo a esa resolucion.
       #La foto original tiene una medida variable, las coordenadas originales no encajarian con 
       #las obtenidas de FB, para ajustar esto se propone
       #una sencilla regla de 3 para reescalar las coordenadas.

       #Se calcula la nueva posicion de la coordenada x con la medida del largo de la imagen original (w)
       posx=face['x']*w/100

       #Se calcula la nueva posicion de la coordenada y con la medida del alto de la imagen original (h)
       posy=face['y']*h/100

       #si la cara reconocida tiene un nombre de usuario se dibuja su nombre de usuario
       if name:
           
           #Imprime el nombre de usuario del rostro detectado
           #print('name: '+name[0]['user']['name'])

           #Se añaden los nombres a una lista
           users.append(name[0]['user']['name'])

           #Dibujamos sobre la imagen un texto con el nombre de usuario
           #draw.text((coordenada_en_x,coordenada_en_y),texto,fill=color_del_texto,font=fuente_de_la_letra)
           draw.text((posx,posy),name[0]['user']['name'],fill='blue',font=font)

           #Para dibujar un rectangulo sobre el rostro tambien hay que escalar las medidas del alto y ancho del rostro detectado
           #(face['width']*w/100) y (face['height']*h/100)
        
           #Dibujamos un rectangulo sobre el rostro        
           #draw.rectangle(((posx+(face['width']*w/100)/2,posy+(face['height']*h/100)/2),(posx-(face['width']*w/100)/2,posy-(face['height']*w/100)/2)),fill=None,outline='red')

       #si no tiene un nombre de usuario entonces es un usuario desconocido
       else:
           draw.text((posx,posy),"usuario no reconocido",fill='blue',font=font)
          
except AttributeError:
   print("verifique las credenciales")
except:
   print("error inesperado, reintente")

#Se importa la lista de personas con acceso al laboratorio
from listaPermitidos import flabianos
flabs=flabianos()

#Busca si los nombres de las personas reconocidas estan dentro de los que tienen acceso
flabs.TuSiTuNo(users)

img.save('save'+str(rank)+'.jpg')

