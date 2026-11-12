from machine import ADC, Pin, PWM
import time


class Photoresistor:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        if min_value >= max_value:
            raise ValueError('Min value is greater or equal to max value')

        self.adc = ADC(Pin(pin))
        # Configura attenuazione per lettura full-scale 0-3.3V (0-4095)
        self.adc.atten(ADC.ATTN_11DB)
        self.min_value = min_value
        self.max_value = max_value
        self.l0 = 0

    def read(self):
        return self.adc.read()

    def value(self):
        return (self.max_value - self.min_value) * self.read() / 4095

    
    def ldr_avvio(self):
        reads = []
        sum = 0
        
        for i in range(20):
            val = self.read()
            reads.append(val)
            sum += val
            utime.sleep_ms(10)
        
        awg = int (sum/20)
        self.l0 = awg
    
    
    def ldr_delta(self):
        return self.read() - self.l0
        
        
            



