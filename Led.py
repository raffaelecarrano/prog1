from machine import Pin#, PWM,ADC
import time
from time import sleep,sleep_ms
class Led:
    def __init__(self, pin):
        self.pin=Pin(pin, Pin.OUT)#necessario Pin.OUT!
        
    def digit_visualizer(self,blink):
        if blink==0:
            self.pin.on()
            sleep_ms(800)
            self.pin.off()
        else:
            for _ in range(blink):
                self.pin.on()
                sleep_ms(100)
                self.pin.off()
                sleep_ms(150)
            
    def good_code(self):
        self.pin.on()
        sleep(2)
        self.pin.off()
        
    def bad_code(self):
        for _ in range(3):
            self.sus(0.5)
            
        for i in range(30):
            for j in range(2):
                self.sus(0.25)
            
    def led_closure(self):
        self.pin.off()
    
    def sus(self,t):
        self.pin.on()
        sleep(t)
        self.pin.off()
        sleep(t)
        
    def sus_condition(self, lettura, soglia):
        if lettura < soglia:
            self.sus(0.5)
    
    
    def led_alarm(self,danger):
        while danger:
            self.sus(0.2)
        
