from machine import Pin, ADC
import time


class Potenziometer:
    def __init__(self,pin):
        self.adc = ADC(Pin(pin, mode=Pin.IN))
        self.adc.atten(ADC.ATTN_11DB)    # Misura 0-3.3V
        
        # inizializzazione cifra corrente all'avvio
        init_value = self.read()
        x = int(10*init_value/4096)
        self.curdigit = min(x,9)
        
    
    def read(self):
        return self.adc.read()
    
    
    def get_cifra(self):
        value = self.read()
        step = 409.6     #ampiezza di un intervallo (4096/10)
        
        if self.curdigit < 9:       # si può salire di intervallo, controlliamo la soglia superiore con isteresi (+15)
            upper = (self.curdigit + 1) * step + 15
            if value >= upper:
                self.curdigit += 1
        
        if self.curdigit > 0:       # si può scendere di intervallo, controlliamo la soglia inferiore con isteresi (-15)
            lower = self.curdigit * step - 15
            if value <= lower:
                self.curdigit -= 1
        
        
        return self.curdigit


    
