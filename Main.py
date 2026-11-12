from Led import Led
from Potenziometer import Potenziometer


from time import sleep
import time
from machine import Pin,PWM,ADC
from enum import Enum

class Stato(Enum):
    BLOCCATO=0
    ACCESSO_CONSENTITO=1
    CAMBIO_CODICE=2
#stati non presenti da specifica
    AVVIO=3
    CHIUSURA=4

##############Gestione Bottone#######################
btn=17
EBOUNCE_MS=200
last_on=0
pressed=false

btn=Pin(btn,Pin.IN,Pin.PULL_DOWN)

def btn_handler(pin):
    global last_on,pressed
    current_time=time.ticks_ms()
    if time.ticks_diff(current_time, last_on) > DEBOUNCE_MS:
        last_on = current_time
        pressed = True

btn.irq(trigger=Pin.IRQ_RISING, handler=btn_handler)
####################################################
buzzer=Buzzer(16)
stepmotor=Stepmotor(33,25,26,27)
servo=Servo(18)
ldr=Photoresistor(32)
ptn=Potenziometer(34)
led=LED_5000hz(14)
initial=[3,7,1,9]
####################################################
last_checked=0
insert=[]
access_count=0
state=Stato.AVVIO
#per lock e unlock
stepper_avviato=False
servo_avviato=False


def routine_inserimento():
    global insert
    global pressed #perchè va modificato
    global state
    state=Stato.AVVIO
    i=0
    while insert.length!=4:
        x=ptn.get_cifra()
        now=time.ticks_ms()
        if pressed and time.ticks_diff(now,last_checked)<15000 :
            insert[i]=x
            led.digit_visualizer(insert[i])
            i+=1
            pressed=false
        if time.ticks_diff(now,last_checked)>=15000:
            print("Inserimento annullato per timeout. (15 secondi)")
            return
 
def unlock():
    global state
    state=Stato.ACCESSO_CONSENTITO
    led.pin.on()
    if servo.angle!=90:
        servo.apply_angle(90)
    #servo.update_servo() va inserito nel main
    #stepper.update() va inserito nel main
    #if !negretti:
        stepper.start_steps(1024,-1)
        

def lock():
    #viene chiamata dopo 10 secondi da avvenuto sblocco nel while
    global state
    state=Stato.CHIUSURA
    led.pin.off()
    stepper.start_steps(1024,1)
    #controllo che stepper abbia finito
    #funzione servo motore
    state=Stato.AVVIO
    
    
    
    
    
 
def auth():
    global initial
    global access_count
    global insert
    global state
    flag=False
    for i in range(4):
        if initial[i]!=insert[i]:
            access_count+=1
            led.bad_code(flag)
            buzzer.codiceErratoTone()
            insert=[0,0,0,0]
            if access_count==3:
                flag=true
                led.bad_code(flag)
                
                now=time.ticks_ms()
                
                print("Sistema temporaneamente bloccato. Timeout: 30 secondi.")
                buzzer.bloccatoTone()
                state=Stato.BLOCCATO
                while(now<30000):
                    continue
            return
    #a questo punto, insert corrisponde a initial: tentativo di accesso riuscito
    state=Stato.ACCESSO_CONSENTITO
    led.good_code()
    buzzer.codiceCorrettoTone()
    access_count=0
    unlock()
            