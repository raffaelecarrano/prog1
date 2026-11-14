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
btn=Pin(17,Pin.IN,Pin.PULL_DOWN)

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


"""
# Meglio se li gestiamo nel while True
def unlock():
    led.pin.on()
    if servo.angle != 90:
        servo.apply_angle(90)
    #servo.update_servo() va inserito nel main
    #stepper.update() va inserito nel main
    #if !negretti:
        stepper.start_steps(1024,-1)
        

def lock():
    #viene chiamata dopo 10 secondi da avvenuto sblocco nel while
    led.pin.off()
    stepper.start_steps(1024,1)
    #controllo che stepper abbia finito
    #funzione servo motore
"""

def auth():
    global access_count, insert, stato_attuale

    if insert == initial:
        print("Accesso autorizzato!")
        buzzer.codiceCorrettoTone()
        led.good_code()
        access_count = 0            # azzero i tentativi
        stato_attuale = APERTURA
    else:
        print("Codice errato!")
        buzzer.codiceErratoTone()
        led.bad_code()
        access_count += 1
        insert = []                # azzero il codice inserito

        if access_count >= 3:
            print("Tre codici errati consecutivi. Sistema Bloccato per 30 s")
            stato_attuale = BLOCCATO
        else:
            stato_attuale = AVVIO


fase_chiusura = 0      
fase_apertura = 0
tempo_sblocco = 0


while True:
    # lettura sensori

    if stato_attuale == AVVIO:
        pass
    elif stato_attuale == ACCESSO_CONSENTITO:
        pass

    # STATO APERTURA
    elif stato_attuale == APERTURA:
        if fase_apertura == 0:
            servo.apply_angle(90)
            fase_apertura = 1
            
        elif fase_apertura == 1:
            servo.update_servo()                        # Fa un passo alla volta ogni 30 ms
            if servo.done:
                stepper.start_steps(1024, -1)           # Senso Orario     
                fase_apertura = 2
                
        elif fase_apertura == 2:
            stepper.update()
            if stepper.done:
                led.pin.on()
                tempo_sblocco = time.ticks_ms()        # Timer di 10 s
                stato_attuale = ACCESSO_CONSENTITO
                fase_apertura = 0

    # STATO: CHIUSURA
    elif stato_attuale == CHIUSURA:
        if fase_chiusura == 0:
            stepper.start_steps(1024, 1)               # Senso Antiorario
            fase_chiusura = 1
            
        elif fase_chiusura == 1:
            stepper.update()
            if stepper.done:
                servo.apply_angle(0)
                fase_chiusura = 2
                
        elif fase_chiusura == 2:
            servo.update_servo()
            if servo.done:
                led.pin.off()
                stato_attuale = AVVIO
                fase_chiusura = 0


    elif stato_attuale == BLOCCATO:
        pass
    elif stato_attuale == CAMBIO_CODICE:
        pass
    elif stato_attuale == PREALLARME:
        pass
    elif stato_attuale == ALLARME:
        pass
    
    
    
    
        
