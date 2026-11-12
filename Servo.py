from machine import Pin,PWM
import utime

# calcoliamo il range su cui opera il servo motore 
# minima posizione (0 gradi) -> duty = durata impulso alto/periodo 0.5ms/20ms = 0.025 = 2.5% duty cycle
# massima posizione (180 gradi) -> duty = durata impulso alto/periodo 2.4ms/20ms = 0.12 = 12% duty cycle

# Risoluzione a 10 bit per duty cycle 0 e 2^10-1 (0-1023).
# 0.025*1023=25.575
# 0.12*1023=122.76


class SERVO:

    def __init__(self,pin):
        self.angle = 0
        self.sg90 = PWM(Pin(pin, mode=Pin.OUT))
        self.sg90.freq(50)
        self.last_move_time = 0
        self.delay = 30 #ms
        self.target = 0
        self.apply_angle(self.angle)
        
    def apply_angle(self, target):
        self.target = target
        
    def update_servo(self):
        """Sposta il servo verso il target con incrementi di 3°"""
        
        if self.angle == self.target:     # già nella posizione richiesta
            return
        
        now = utime.ticks_ms()
        
        if utime.ticks_diff(now, self.last_move_time) >= self.delay:
            self.last_move_time = now
            
            if self.target > self.angle:
                self.angle += min(3, self.target - self.angle)
            else:
                self.angle -= min(3, self.angle - self.target)
        
            duty = int(22 + (self.angle/180)*100)  # Mappatura lineare: 0° -> 22, 180° -> 122 (circa)
            self.sg90.duty(duty)
        
        
        
    
    
            
        
