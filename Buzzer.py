from machine import Pin, PWM
from time import sleep_ms


class BUZZER:
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))
        self.pwm.duty(0)
        
# 1 beep,1000,200 ms; 2 beep,1500,100ms (AUTO); 1 beep,2000Hz,300ms(MANUAL)
# 3 beep,800,150ms(Low light alarm)
# nota: duty è fissato a 512
    def beep(self, freq, durata, duty=512):
        self.pwm.freq(freq)
        self.pwm.duty(duty)
        time.sleep_ms(durata)
        self.stop()
# funzioni che chiamano la beep
    def suono_avvio(self):
        self.beep(freq=1000,durata=200)
        
    def suono_auto(self):
        self.beep(freq=1500,durata=100)
        time.sleep_ms(100)
        self.beep(freq=1500,durata=100)
        time.sleep_ms(100)
        
    def suono_manuale(self):
        self.beep(freq=2000,durata=300)
        
    def allarme(self):
        for _ in range(3):
            self.beep(freq=800,durata=150)
            time.sleep_ms(100)

    def stop(self):
        self.pwm.duty(0)
        


