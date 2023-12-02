import pyb, os
from pyb import RTC, Pin
import time
import pyb
import machine

p1 = pyb.Pin(pyb.Pin.cpu.A2, pyb.Pin.IN, pyb.Pin.PULL_UP)
p2 = pyb.Pin(pyb.Pin.cpu.A3, pyb.Pin.IN, pyb.Pin.PULL_UP)
p3 = pyb.Pin(pyb.Pin.cpu.A4, pyb.Pin.IN, pyb.Pin.PULL_UP)
p4 = pyb.Pin(pyb.Pin.cpu.A5, pyb.Pin.IN, pyb.Pin.PULL_UP)

# Configuración de pines
pines_a_monitorear = [p1, p2, p3, p4]
contador = [0, 0, 0, 0]
tiempo_inicio = [0, 0, 0, 0]
tiempo_transcurrido=[0, 0, 0, 0]
#estado_actual = [0, 0, 0, 0]
#estados_anteriores = [0, 0, 0, 0]
# Configuración de tiempo límite en segundos
tiempo_limite = 3000

# Configuración de la ruta del archivo en la tarjeta microSD
ruta_archivo = "/sd/registro_estado.txt"

# Inicializar la tarjeta microSD
sd = pyb.SDCard()
os.mount(sd, "/sd")
led1 = pyb.LED(1)
led2 = pyb.LED(2)


# Función para registrar el cambio de estado de alto a bajo
def registrar_cambios_estado():
    estados_anteriores = [pin.value() for pin in pines_a_monitorear]  
    while True:
           
        for i, pin in enumerate(pines_a_monitorear):
            time.sleep_ms(100)

            estado_actual = [pin.value() for pin in pines_a_monitorear]
            if estado_actual[i] == 0 and estados_anteriores[i] == 1:
                tiempo_inicio[i] = time.ticks_ms()
                led2.on()
                
            estado_actual = [pin.value() for pin in pines_a_monitorear]
            if estado_actual[i] == 1 and estados_anteriores[i] == 0 and time.ticks_diff(time.ticks_ms(), tiempo_inicio[i]) > tiempo_limite:
                contador[i] += 1
                tiempo = time.ticks_diff(time.ticks_ms(), tiempo_inicio[i])/1000
                with open(ruta_archivo, "a") as archivo:
                    fecha_hora = time.localtime()
                    archivo.write('Pin: ' + str(i) + ' cont: ' + str(contador[i])+ ' tiempo: ' + str(tiempo)+'\n')
                    led2.off()
                
                    
               
            estados_anteriores[i] = estado_actual[i]
            
# Llamar a la función para registrar el cambio de estado
registrar_cambios_estado()