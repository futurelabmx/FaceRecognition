#Para dibujar rectangulos y nombres sobre las caras
from PIL import Image, ImageDraw, ImageFont

#Insert your access token obtained from Graph API explorer here
TOKEN='EAAE3nyZCkZBS0BAAunHtMQK6TFdSct2ZCtsfIAixn9QZAiMfxMYRhZChre6vAEZCDcOjZCkH5etZBix25fnFutscjkAqFnwQJ8hgN3nNiKjJaoZBYvaHw9gnhfohfaK9LntaNPS2abJVPvkCcvCLtdNVd3j9uFFz1QaZASKOzij5QNNvhShnkhWocnfeJoni4np5kZD' 

# Insert your cookie string here
COOKIE='datr=WOy-WfHNoH9xZxDWb_h499W7; sb=WOy-WR642QFFfyPxCRfeOoEr; c_user=100001064064854; xs=4%3A1o7U2CQ11BTGDw%3A2%3A1505687159%3A13666%3A11901; ; fr=0xS2BKjrtVCbuVmjp.AWXqF9Rw-FKwH9xap_-sQHtS6ew.BZvuxY.I8.FqV.0.0.Balbnt.; act=1519765291621%2F2; wd=575x662; presence=EDvF3EtimeF1519765314EuserFA21B01064064854A2EstateFDt3F_5b_5dG519765314354CEchFDp_5f1B01064064854F14CC'

# Insert the fb_dtsg parameter obtained from Form Data here.
FB_DTSG='AQF3FM3TklNW:AQF_ijFzbZww'

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


def wrapper(photo,access_token,cookie,fb_dtsg):
    #An unofficial python wrapper for the Facebook face recognition endpoint
    from fbrecog import FBRecog
    
    # Instantiate the recog class
    recog = FBRecog(access_token, cookie, fb_dtsg)

    # Recog class can be used multiple times with different paths
    #print(recog.recognize(photo))    

    #print('-'*40)
    # Call recognize_raw to get more info about the faces detected, including their positions
    #print(recog.recognize_raw(photo))

    faces = recog.recognize_raw(path)
    result=[]
    for face in faces:
        name=face['recognitions']    
        if name:
            print('name: '+name[0]['user']['name'])
            posx=face['x']*w/100        
            posy=face['y']*h/100
            size=face['width']*face['height']
            plt.text(posx,posy,name[0]['user']['name'])
            draw.text((posx,posy),name[0]['user']['name'],fill='blue',font=font)
            plt.scatter(posx, posy, s=np.pi*size, c='white', alpha=0.30) #transparencia del 0.10 (1 es opaco y 0 es transparente)
            draw.rectangle(((posx+(face['width']*w/100)/2,posy+(face['height']*h/100)/2),(posx-(face['width']*w/100)/2,posy-(face['height']*w/100)/2)),fill=None,outline='red')

    plt.imshow(background)
    img.save('reconocidos.jpg')
