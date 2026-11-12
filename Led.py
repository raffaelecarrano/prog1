
from machine import Pin
import time


class Led:

    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.off()

        self.active = False
        self.is_on = False

        self.mode = None

        self.deadline = 0

        self.on_time = 0
        self.off_time = 0

        self.remaining = 0
        self.frequency = 0

    # --------------------------------
    # GESTIONE SEQUENZE TEMPORALI
    # --------------------------------

    def _start(self, on_time, off_time, repetitions=0):
        self.stop()

        self.on_time = on_time
        self.off_time = off_time
        self.remaining = repetitions

        self.active = True
        self.is_on = True

        self.pin.on()

        self.deadline = time.ticks_add(
            time.ticks_ms(), on_time
        )

        self.mode = "sequence"

    # --------------------------------
    # CODICE CORRETTO
    # --------------------------------

    def good_code(self):
        # LED acceso fisso per 2 secondi
        self._start(2000, 0, 1)

    # --------------------------------
    # CODICE ERRATO
    # --------------------------------

    def bad_code(self, flag):

        if flag:
            # 2 Hz per 30 secondi:
            # 250 ms acceso + 250 ms spento
            self.stop()

            self.active = True
            self.mode = "timed_blink"

            self.on_time = 250
            self.off_time = 250

            self.remaining = 60

            self.is_on = True
            self.pin.on()

            self.deadline = time.ticks_add(
                time.ticks_ms(), 250
            )

        else:
            # 3 lampeggi rapidi
            self._start(100, 100, 3)

    # --------------------------------
    # PREALLARME
    # --------------------------------

    def preallarm(self):
        # Periodo totale 1000 ms
        # 500 ms acceso + 500 ms spento
        self.stop()

        self.active = True
        self.mode = "continuous"

        self.on_time = 500
        self.off_time = 500

        self.is_on = True
        self.pin.on()

        self.deadline = time.ticks_add(
            time.ticks_ms(), 500
        )

    # --------------------------------
    # ALLARME
    # --------------------------------

    def allarm(self):
        # Periodo totale 200 ms
        # 100 ms acceso + 100 ms spento
        self.stop()

        self.active = True
        self.mode = "continuous"

        self.on_time = 100
        self.off_time = 100

        self.is_on = True
        self.pin.on()

        self.deadline = time.ticks_add(
            time.ticks_ms(), 100
        )

    # --------------------------------
    # AGGIORNAMENTO NON BLOCCANTE
    # --------------------------------

    def update(self):

        if not self.active:
            return

        now = time.ticks_ms()

        if time.ticks_diff(now, self.deadline) < 0:
            return

        if self.is_on:

            # Spegne il LED
            self.pin.off()
            self.is_on = False

            if self.mode == "sequence" or self.mode == "timed_blink":
                self.remaining -= 1

                if self.remaining <= 0:
                    self.stop()
                    return

            self.deadline = time.ticks_add(
                now, self.off_time
            )

        else:

            # Riaccende il LED
            self.pin.on()
            self.is_on = True

            self.deadline = time.ticks_add(
                now, self.on_time
            )

    # --------------------------------
    # STOP
    # --------------------------------

    def stop(self):

        self.pin.off()

        self.active = False
        self.is_on = False

        self.remaining = 0
        self.mode = None

    def deinit(self):
        self.stop()
        self.pin = None

'''
good_code(self): fa rimanere il led acceso per 2 secondi
bad_code(self,flag): fa eseguire tre lampeggi rapidi al led se il flag è false e lampeggia con freq di 2hz per 30secondi
preallarm(slef): fa lampeggiare il led con un periodo di 1000ms fino alla stop()
allarm(self): fa lampeggiare il led rapidamente con periodi di 200ms fino alla stop()
stop(slef): fa fermare il led
update(self): per aggiornare il time
'''
