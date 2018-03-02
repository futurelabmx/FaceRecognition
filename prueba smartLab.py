#Para dibujar rectangulos y nombres sobre las caras
from PIL import Image, ImageDraw, ImageFont

#Insert your access token obtained from Graph API explorer here
TOKEN='EAAE3nyZCkZBS0BADghixcHvasHswvpA95guBOMfTG8SoqemCA6Wn8aLxYCJNJCvorFuypsvdxfdFMkeszZCQiYrZAvo62RjCvN7ClLpakld5Wos8bZB4Ai5N2J7jUSxhn9HBnbJyu90gFtkBSJjpMQxFSiNDaQaacq1m0SNkfhaWEa0iOQVZAJhRx4f8CYZA98ZD' 

# Insert your cookie string here
COOKIE='datr=WOy-WfHNoH9xZxDWb_h499W7; sb=WOy-WR642QFFfyPxCRfeOoEr; ; locale=es_LA; c_user=100001064064854; xs=37%3AKZeQpHc9CQwHGw%3A2%3A1519939628%3A13666%3A11901; fr=0xS2BKjrtVCbuVmjp.AWWcd0XkFXPl0iyyaF3fD4ZI2K4.BZvuxY.I8.FqV.0.0.BamHAs.AWWiGoqJ; pl=n; presence=EDvF3EtimeF1519939640EuserFA21B01064064854A2EstateFDutF1519939640953CEchFDp_5f1B01064064854F2CC; act=1519939693689%2F2; wd=871x662'

# Insert the fb_dtsg parameter obtained from Form Data here.
FB_DTSG='AQHAOAJZ5Lor:AQGJ2qbYJkjZ'

# Insert your image file path here    
photo='amigos.jpg'

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
