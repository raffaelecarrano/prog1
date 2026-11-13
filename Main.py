from Led import Led
from Potenziometer import Potenziometer

from time import sleep
import time
from machine import Pin,PWM,ADC
from enum import Enum

# STATI
BLOCCATO=0
ACCESSO_CONSENTITO=1
CAMBIO_CODICE=2
#stati non presenti da specifica
AVVIO=3
CHIUSURA=4
APERTURA=5
PREALLARME=6
ALLARME=7

##############Gestione Bottone#######################
btn=Pin(btn,Pin.IN,Pin.PULL_DOWN)

DEBOUNCE_MS=200
last_on=0
pressione=False
pressione_lunga=False
btn_ultimo_stato=0
btn_inizio_pressione=0


def btn_handler(pin):
    global last_on, pressione, pressione_lunga, btn_ultimo_stato, btn_inizio_pressione
    now=time.ticks_ms()
    valore_attuale = btn.value()

    if valore_attuale != btn_ultimo_stato and time.ticks_diff(now, last_on) > DEBOUNCE_MS:
        last_on = now
        btn_ultimo_stato = valore_attuale

        if valore_attuale == 1:
            btn_inizio_pressione = now
        else:
            durata = time.ticks_diff(now, btn_inizio_pressione)
            if durata >= 3000:
                pressione_lunga = True
            elif durata > 200:
                pressione = True

####################################################
buzzer=Buzzer(16)
stepmotor=Stepmotor(33,25,26,27)
servo=Servo(18)
ldr=Photoresistor(32)
ptn=Potenziometer(34)
led=LED_5000hz(14)
initial=[3,7,1,9]
####################################################
insert=[]
access_count=0
stato_attuale = AVVIO
tempo_inizio_timeout = 0

def routine_inserimento():
    global insert, pressione, stato_attuale, tempo_inizio_timeout

    insert = []
    tempo_inizio_timeout = time.ticks_ms()       # inizializza il timer dei 15s all'ingresso
    
    while len(insert) < 4:
        now = time.ticks_ms()
        x=ptn.get_cifra()

        if time.ticks_diff(now, tempo_inizio_timeout) >= 15000:
            print("Inserimento annullato per timeout. (15 s)")
            insert = []
            return

        btn_handler()
        if pressione:
            pressione = False
            insert.append(x)
            print(f"Codice attuale: {insert}")
            led.digit_visualizer(x)
            tempo_inizio_timeout = now



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
            
