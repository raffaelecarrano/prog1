from machine import Pin
import time

class Led:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.off()
        
        # Variabili di stato temporale per l'esecuzione non bloccante
        self.last_tick = time.ticks_ms()
        self.t_on = 0            # Durata accensione (ms)
        self.t_off = 0           # Durata spegnimento (ms)
        self.repeats_left = 0    # Cicli rimanenti
        self.is_on = False       # Stato logico corrente del LED
        self.active = False      # Indica se c'è una sequenza in corso

    def update(self):
        """Metodo da chiamare a ogni iterazione del ciclo principale (while True)."""
        if not self.active:
            return

        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, self.last_tick)

        if self.is_on:
            # Se è trascorso il tempo di ON, spegne il LED
            if elapsed >= self.t_on:
                self.pin.off()
                self.is_on = False
                self.last_tick = now
                self.repeats_left -= 1
        else:
            # Se è trascorso il tempo di OFF
            if elapsed >= self.t_off:
                if self.repeats_left > 0:
                    # Inizia il prossimo ciclo ON
                    self.pin.on()
                    self.is_on = True
                    self.last_tick = now
                else:
                    # Sequenza completata
                    self.active = False
                    self.pin.off()

    def _start_pattern(self, t_on, t_off, count):
        """Configura e avvia un pattern senza fermare l'esecuzione."""
        if count <= 0:
            self.led_closure()
            return
        self.t_on = t_on
        self.t_off = t_off
        self.repeats_left = count
        self.pin.on()
        self.is_on = True
        self.active = True
        self.last_tick = time.ticks_ms()

    def digit_visualizer(self, blink):
        if blink == 0:
            # 1 lampeggio da 800 ms (0 ms di pausa successiva)
            self._start_pattern(800, 0, 1)
        else:
            # 'blink' lampeggi da 100 ms con pausa di 150 ms
            self._start_pattern(100, 150, blink)

    def good_code(self):
        # Acceso per 2000 ms (2 secondi) e poi spento
        self._start_pattern(2000, 0, 1)

    def bad_code(self):
        # 3 lampeggi da 1 secondo (1000 ms ON, 1000 ms OFF)
        self._start_pattern(1000, 1000, 3)

    def sus(self, t):
        # Converte t (secondi) in millisecondi
        ms = int(t * 1000)
        self._start_pattern(ms, ms, 1)

    def sus_condition(self, lettura, soglia):
        if lettura < soglia and not self.active:
            self.sus(0.5)

    def led_alarm(self, danger):
        if danger and not self.active:
            self.sus(0.2)

    def led_closure(self):
        self.active = False
        self.is_on = False
        self.repeats_left = 0
        self.pin.off()