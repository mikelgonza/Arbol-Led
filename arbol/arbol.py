import requests
import time
import board
import neopixel
import keyboard
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions


# API
url = "https://api.wfuneralnet.com/arbol"
color = (0,0,0)
nombre = ""

# Neopixel
# Manzanas
pin_manzanas = board.D21
num_pixels = 100
ORDER = neopixel.GRB

# Definir objeto manzanas
manzanas = neopixel.NeoPixel(
    pin_manzanas, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


# Apagar pixeles
manzanas.show()


    
# RGB-Matrix P4 32x64
options = RGBMatrixOptions()
options.gpio_slowdown = 2
options.cols = 64
matrix = RGBMatrix(options = options)

canvas1 = matrix
canvas2 = matrix
canvas3 = matrix

textAmarillo = graphics.Color(255, 255, 0)
textVerde = graphics.Color(0,255,0)
textAzul = graphics.Color(0, 0, 255)
textRojo = graphics.Color(255, 0, 0)

fuente1 = graphics.Font()
fuente1.LoadFont("fonts/texgyre-27.bdf")

fuente2 = graphics.Font()
fuente2.LoadFont("fonts/7x13.bdf")

# Funcion que gestiona las manzanas, recibe el id y el color
def manzana(id, color=(0,0,0)):
    a = b = 0
    
    # Definimos el rango de los leds en toda la tira segun el id
    if id == 1: a=0; b=8
    if id == 2: a=8; b=16
    if id == 3: a=16; b=24
    if id == 4: a=24; b=32
    if id == 5: a=32; b=40
    if id == 6: a=40; b=48
    if id == 7: a=48; b=56
    if id == 8: a=56; b=64
    if id == 9: a=64; b=72
    if id == 10: a=72; b=80
    
    # Aplicamos el color a los leds del rango obtenido
    for i in range(a,b):
        manzanas[i] = color

    # Encendemos leds
    manzanas.show()
    



while True:
    
    #Leemos json
    data = requests.get(url)
    json = data.json()
    
    # Guardamos variables principales
    nombre = json["nombre"]
    desc = "Funeraria"
    desc2 = "Bilbao"
    #print("Nombre:", nombre)
    
    # Escribimos texto en panel led
    graphics.DrawText(canvas1, fuente2, 1, 9, textVerde, nombre)
    graphics.DrawText(canvas2, fuente2, 1, 20, textAzul, desc)
    graphics.DrawText(canvas3, fuente2, 1, 31, textRojo, desc2)
    
    # Recorremos las manzanas
    for i in json["manzanas"]:
        
        # Guardamos variables
        activo = i["activo"]
        id = i["id"]
        
        # Comprobar que los valores rgb no tienen error
        r=i["colorR"]            
        g=i["colorG"]
        b=i["colorB"]
        if not isinstance(r, int) or r < 0 or r > 255: r = 0
        if not isinstance(g, int) or g < 0 or g > 255: g = 0
        if not isinstance(b, int) or b < 0 or b > 255: b = 0 
        color = (r, g, b)
        
        #print("activo:",activo)
        #print("color:",color)
        #print("id:",id)
        
        # Mandamos encender manzanas si el id es correcto
        if id >= 1 and id <= 10:
            if activo:
                manzana(id, color)
            else:
                manzana(id)
    
    # Tiempo de espera de cada ciclo
    #time.sleep(5)
        
