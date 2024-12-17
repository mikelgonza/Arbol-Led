import requests
import time
import board
import neopixel
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image
from threading import Thread



def main():
    
    # API
    url = "https://api.celebrasuvida.es/arbol"
    color = (0,0,0)
    nombre = ""
    nombre2 = ""

    # Neopixel
    # Manzanas
    pin_manzanas = board.D21
    num_pixels = 100
    ORDER = neopixel.GRB

    # Objeto manzanas
    manzanas = neopixel.NeoPixel(
        pin_manzanas, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )


    # Apagar pixeles
    manzanas.show()


    # RGB-Matrix P4 32x64
    # Opciones del panel
    options = RGBMatrixOptions()
    options.gpio_slowdown = 2
    options.cols = 64
    matrix = RGBMatrix(options = options)
    
    logo_albia = Image.open("logo2.png")
    

    # Colores texto panel
    amarillo = graphics.Color(255, 255, 0)
    verde = graphics.Color(0,255,0)
    azul = graphics.Color(0, 0, 255)
    rojo = graphics.Color(255, 0, 0)
    blanco = graphics.Color(255,255,255)

    fuente1 = graphics.Font()
    fuente1.LoadFont("fonts/6x13.bdf")

    fuente2 = graphics.Font()
    fuente2.LoadFont("fonts/7x13B.bdf")
   
    
    # Funcion para encender el tronco
    def tronco(color=(0,0,0)):
        a=80; b=96
        
        # Apagamos tronco
        for i in range(a,b):
            manzanas[i] = (0,0,0)
        manzanas.show()
        
        # Encendemos tronco
        for i in range(a,b):
            manzanas[i] = color
            manzanas.show()
            time.sleep(0.07)
            

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
    
    def manzanaBlink(id, color=(0,0,0)):
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

        # Hacemos parpadeo hasta que se pare el hilo
        while not stop_manzanaBlink:
            
            # Encendemos leds
            for i in range(a,b):
                manzanas[i] = color
            manzanas.show()

            time.sleep(0.5)

            # Apagamos leds
            for i in range(a,b):
                manzanas[i] = (0,0,0)
            manzanas.show()

            time.sleep(0.5)
        
       
    def hilo2(nombre, texto):
        
        # Objetos texto panel
        panel_nombre = matrix
        panel_texto = matrix.CreateFrameCanvas()
        
        pos = 64
        
        panel_nombre.Clear()

        if nombre == "ALBIA":
            # Logo Albia
            matrix.SetImage(logo_albia.convert('RGB'), 0, 7)

        else:

            while not stop_hilo2:
                        
                panel_texto.Clear()

                # Preparamos texto
                len = graphics.DrawText(panel_texto, fuente2, pos, 29, verde, texto)
                pos -= 1
                if (pos + len < 0):
                    pos = panel_texto.width

                panel_texto = matrix.SwapOnVSync(panel_texto)
        
                # Preparamos nombre
                # Si el nombre es mas largo de 8 hacemos scroll, sino queda fijo
                if (nombre.__len__() > 9):
                    pos2 = pos
                else:
                    pos2 = 1
                    
                graphics.DrawText(panel_nombre, fuente1, pos2, 16, blanco, nombre)
                    
                time.sleep(0.05)
        
    
    nombre_anterior = ""
    texto_anterior = ""
    primer_ciclo = True
    primera_manzana = True
    id_blink = 0
    id_blink_anterior = 0

    # Bucle principal
    while True:

        stop_hilo2 = False
        stop_manzanaBlink = False
        
        #Leemos json
        data = requests.get(url)
        print("Conectando API...")
        
        # Si hay fallo en la conexion reintentamos en 5 segundos
        while data.status_code != 200:
            print("Error de conexion:",requests.status_code)
            time.sleep(5)
            data = requests.get(url)
        
        # Recogemos el json
        print("API conectada")
        json = data.json()
              
        
        # Variables texto panel
        nombre = json["nombre"]
        texto = json["texto"]
        
        
        # Comprobamos si hay cambios en el nombre
        if (nombre_anterior != nombre or texto_anterior != texto):
            
            # En el primer ciclo mandamos el texto
            if primer_ciclo == 1:
                
                print("Primer ciclo, mandamos texto")
                # Iniciamos hilo2 y mandamos mensaje
                thread = Thread(target=hilo2, args=(nombre, texto))
                thread.start()
            
            # si no es el primer ciclo, paramos hilo2 y mandamos nuevo texto
            else:
                print("Texto cambiado, paramos hilo2")
                stop_hilo2 = True
                while thread.is_alive():
                    time.sleep(0.05)
                
                stop_hilo2 = False
                
                # Iniciamos hilo2
                print("Mandamos texto con nuevos datos")
                thread = Thread(target=hilo2, args=(nombre, texto))
                thread.start()
                

        nombre_anterior = nombre
        texto_anterior = texto
        
        # Encendemos tronco
        tronco((255,255,255))
        
        # Encendemos manzanas
        for i in json["manzanas"]:
            
            # Guardamos variables
            activo = i["activo"]
            id = i["id"]
            blink = i["blink"]
            
            # Comprobar que los valores rgb no tienen error
            r=i["colorR"]            
            g=i["colorG"]
            b=i["colorB"]
            if not isinstance(r, int) or r < 0 or r > 255: r = 0
            if not isinstance(g, int) or g < 0 or g > 255: g = 0
            if not isinstance(b, int) or b < 0 or b > 255: b = 0 
            color = (r, g, b)
                    
            # Mandamos encender manzanas si el id es correcto
            if (id >= 1 and id <= 10):
                if activo:
                    manzana(id, color)
                    print("Encender manzana", id, )
                else:
                    manzana(id)
                
                if blink:
                    id_blink = id
                    if primera_manzana == True:
    
                        print("Primera manzana, mandamos parpadeo")
                        # Iniciamos hilo2 y mandamos mensaje
                        thread2 = Thread(target=manzanaBlink, args=(id, color))
                        thread2.start()

                        primera_manzana = False
                    else:
                        if id_blink != id_blink_anterior:
                            print("Blink manzana cambiada, paramos manzanaBlink")
                            stop_manzanaBlink = True
                            while thread2.is_alive():
                                time.sleep(0.05)
                            
                            manzana(id_blink_anterior, color_anterior)
                            stop_manzanaBlink = False
                            
                            # Iniciamos hilo2
                            print("Mandamos parpadeo de la nueva manzana")
                            thread2 = Thread(target=manzanaBlink, args=(id, color))
                            thread2.start()
                    
                    id_blink_anterior = id_blink
                    color_anterior = id_blink
     
        
        # Tiempo de espera de cada ciclo
        time.sleep(10)

        primer_ciclo = False
        print("Reiniciamos bucle principal")
      
        

if __name__ == '__main__':
    main()
