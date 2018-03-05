
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
       i+=1
       
       if i>5: #esperamos a que se estabilice la imagen para guardar una fotografia
           cv2.imwrite('save.jpg', img)       
       break
   
   #Mostramos la imagen
   #cv2.imshow('img',img)   
   
   #con la tecla 'q' salimos del programa
   #if cv2.waitKey(1) & 0xFF == ord('q'):
   #    break

   #detenemos el bucle para buscar caras
   break

cap.release()
cv2.destroyAllWindows()


#INICIO DE FBRECOG PARA RECONOCIMIENTO FACIAL
#Para dibujar rectangulos y nombres sobre las caras
from PIL import Image, ImageDraw, ImageFont

#Insert your access token obtained from Graph API explorer here
TOKEN='EAAE3nyZCkZBS0BAN6LapGqut1cgm9lPMTQGiZBu86e2fEVoNDUowR7lo2M4rbuUDPIB9KcZA8EI5t8JUGm6Y5OHJsysWD2PspgnHPk7JqgxBDN1GlYyZCIIBlSBhNmZCG7S36RZAxgBqOLSfqdZAB7kr7FR9A2uLLSUhNPhU9mLzaV4bA6H8RqnessUtYoqhp6gZD' 

# Insert your cookie string here
COOKIE='datr=WOy-WfHNoH9xZxDWb_h499W7; sb=WOy-WR642QFFfyPxCRfeOoEr; locale=es_LA; c_user=100001064064854; xs=37%3AKZeQpHc9CQwHGw%3A2%3A1519939628%3A13666%3A11901; pl=n; fr=0xS2BKjrtVCbuVmjp.AWUcwaiKXmar99cMBVi30J26r7s.BZvuxY.I8.FqV.0.0.BamYB4.AWWMiZpK; act=1520260843130%2F3; presence=EDvF3EtimeF1520260846EuserFA21B01064064854A2EstateFDutF1520260846394CEchFDp_5f1B01064064854F4CC; wd=871x662'

# Insert the fb_dtsg parameter obtained from Form Data here.
FB_DTSG='AQFIJ_sh_V20:AQE6qXPvXDC3'

# Insert your image file path here    
photo='save1.jpg'

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

faces = recog.recognize_raw(photo)
result=[]
for face in faces:
    
    name=face['recognitions']    
    if name:
        #print('name: '+name[0]['user']['name'])
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 500  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        winsound.Beep(frequency, duration)
        
        posx=face['x']*w/100
        posy=face['y']*h/100
        size=face['width']*face['height']        
        draw.text((posx,posy),name[0]['user']['name'],fill='#0033e7',font=font)
        draw.rectangle(((posx+(face['width']*w/100)/2,posy+(face['height']*h/100)/2),(posx-(face['width']*w/100)/2,posy-(face['height']*w/100)/2)),fill=None,outline='red')

img.save('reconocidos.jpg')

