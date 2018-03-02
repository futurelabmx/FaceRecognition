#Para dibujar rectangulos y nombres sobre las caras
from PIL import Image, ImageDraw, ImageFont

#Insert your access token obtained from Graph API explorer here
TOKEN='xxxx' 

# Insert your cookie string here
COOKIE='xxxx'

# Insert the fb_dtsg parameter obtained from Form Data here.
FB_DTSG='xxxx'

# Insert your image file path here    
photo='xxxx.jpg'

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
        posx=face['x']*w/100        
        posy=face['y']*h/100
        size=face['width']*face['height']        
        draw.text((posx,posy),name[0]['user']['name'],fill='blue',font=font)        
        draw.rectangle(((posx+(face['width']*w/100)/2,posy+(face['height']*h/100)/2),(posx-(face['width']*w/100)/2,posy-(face['height']*w/100)/2)),fill=None,outline='red')

img.save('reconocidos.jpg')
