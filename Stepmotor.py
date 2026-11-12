import utime
from machine import Pin

class STEPMOTOR:
    # Sequenze di attivazione dei passi
    step_sequence = [
        [1, 0, 0, 1],  
        [1, 1, 0, 0],  
        [0, 1, 1, 0],  
        [0, 0, 1, 1],  
    ]

    step_sequence_half = [
        [1, 0, 0, 0],  # solo IN1
        [1, 0, 0, 1],  # IN1+IN4
        [0, 0, 0, 1],  # solo IN4
        [0, 0, 1, 1],  # IN3+IN4
        [0, 0, 1, 0],  # solo IN3
        [0, 1, 1, 0],  # IN2+IN3
        [0, 1, 0, 0],  # solo IN2
        [1, 1, 0, 0],  # IN1+IN2
    ]

    def __init__(self, pin1, pin2, pin3, pin4):
        self.stepper_pins = [Pin(pin1, Pin.OUT), Pin(pin2, Pin.OUT), Pin(pin3, Pin.OUT), Pin(pin4, Pin.OUT)]
        self.step_index = 0
        self.sequence = self.step_sequence_half
        self.target_steps = 0
        self.last_step_time = 0
        self.step_delay = 3 # ms
        
        
    def start_steps(self, steps, direction):
        """Avvia la richiesta di movimento senza bloccare il codice"""
        self.target_steps = steps
        self.direction = direction
        
    
    def update(self):
        """Esegue un solo passo"""
        if self.target_steps <= 0:
            return

        now = utime.ticks_ms()
        if utime.ticks_diff(now, self.last_step_time) >= self.step_delay:
            self.last_step_time = now
            
            # Esegue un passo
            self.step_index = (self.step_index + self.direction) % len(self.sequence)
            
            for pin_index in range(len(self.stepper_pins)):
                pin_value = self.sequence[self.step_index][pin_index]
                self.stepper_pins[pin_index].value(pin_value)
                
            self.target_steps -= 1
            

    def stop(self):
        """Spegne tutte le bobine"""
        self.target_steps = 0
        
        for pin in self.stepper_pins:
            pin.value(0)

