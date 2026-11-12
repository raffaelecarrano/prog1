from machine import Pin
import time

class Led:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.off()
        
        # Variabili di stato temporale
        self.last_tick = time.ticks_ms()
        self.is_on = False
        self.pattern_queue = []   # Coda delle fasi: [(t_on, t_off, count), ...]
        self.curr_t_on = 0
        self.curr_t_off = 0
        self.repeats_left = 0
        self.active = False
        self.alarm_active = False

    def update(self):
        """Da invocare a ogni giro del while True nel main."""
        # Se non c'è una fase attiva ma c'è roba in coda, carica la prossima fase
        if not self.active and self.pattern_queue:
            self._load_next_stage()

        # Se l'allarme continuo è attivo e non c'è nulla in corso, rilancia il blink
        if not self.active and self.alarm_active:
            self.sus(0.2)
            return

        if not self.active:
            return

        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, self.last_tick)

        if self.is_on:
            if elapsed >= self.curr_t_on:
                self.pin.off()
                self.is_on = False
                self.last_tick = now
                self.repeats_left -= 1
        else:
            if elapsed >= self.curr_t_off:
                if self.repeats_left > 0:
                    self.pin.on()
                    self.is_on = True
                    self.last_tick = now
                else:
                    self.active = False
                    self.pin.off()
                    # Se ci sono altre fasi in coda (es. bad_code), avvia subito la successiva
                    if self.pattern_queue:
                        self._load_next_stage()

    def _load_next_stage(self):
        t_on, t_off, count = self.pattern_queue.pop(0)
        self.curr_t_on = t_on
        self.curr_t_off = t_off
        self.repeats_left = count
        self.pin.on()
        self.is_on = True
        self.active = True
        self.last_tick = time.ticks_ms()

    def _set_sequence(self, stages):
        self.pattern_queue = stages.copy()
        self.active = False
        self.is_on = False
        self._load_next_stage()

    def digit_visualizer(self, blink):
        if blink == 0:
            self._set_sequence([(800, 0, 1)])
        else:
            self._set_sequence([(100, 150, blink)])

    def good_code(self):
        self._set_sequence([(2000, 0, 1)])

    def bad_code(self, flag):
        if flag:
            # 60 lampeggi (30 * 2) da 0.25 s (250 ms ON, 250 ms OFF)
            stages = [(250, 250, 60)]
        else:
            # 3 lampeggi da 0.5 s (500 ms ON, 500 ms OFF)
            stages = [(500, 500, 3)]
            
        self._set_sequence(stages)
    

    def sus(self, t):
        ms = int(t * 1000)
        self._set_sequence([(ms, ms, 1)])

    def sus_condition(self, lettura, soglia):
        if lettura < soglia and not self.active:
            self.sus(0.5)

    def led_alarm(self, danger):
        self.alarm_active = danger
        if not danger:
            self.led_closure()

    def led_closure(self):
        self.pattern_queue.clear()
        self.alarm_active = False
        self.active = False
        self.is_on = False
        self.repeats_left = 0
        self.pin.off()