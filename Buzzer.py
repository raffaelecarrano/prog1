
from machine import Pin, PWM
import time


class Buzzer:

    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty(0)
        self.buzzer.freq(0)

        self.active = False
        self.beep_on = False

        self.remaining = 0
        self.deadline = 0

        self.frequency = 0
        self.duration = 0
        self.interval = 0
        self.pause = 0

        self.mode = None
        self.frequency2 = 0
        self.current_frequency = 0

    def _start(self, frequency, duration, repetitions, pause=100):
        self.stop()

        self.frequency = frequency
        self.duration = duration
        self.remaining = repetitions
        self.pause = pause

        self.current_frequency = frequency
        self.buzzer.freq(frequency)
        self.buzzer.duty(512)

        self.beep_on = True
        self.active = True
        self.mode = "normal"

        self.deadline = time.ticks_add(
            time.ticks_ms(), duration
        )

    # --------------------------------
    # SUONI SINGOLI / RIPETUTI
    # --------------------------------

    def codiceCorrettoTone(self):
        # 2 beep da 1500 Hz, 150 ms
        self._start(1500, 150, 2, 100)

    def codiceErratoTone(self):
        # 1 beep da 400 Hz, 500 ms
        self._start(400, 500, 1)

    def cambioCodiceTone(self):
        # 3 beep da 1800 Hz, 100 ms
        self._start(1800, 100, 3, 100)

    # --------------------------------
    # SUONI PERIODICI
    # --------------------------------

    def _startPeriodic(self, frequency, duration, interval):
        self.stop()

        self.frequency = frequency
        self.duration = duration
        self.interval = interval

        self.active = True
        self.beep_on = True
        self.mode = "periodic"

        self.buzzer.freq(frequency)
        self.buzzer.duty(512)

        self.deadline = time.ticks_add(
            time.ticks_ms(), duration
        )

    def bloccatoTone(self):
        # Beep da 800 Hz ogni 5 secondi
        self._startPeriodic(800, 100, 5000)

    def sospettaIntrusioneTone(self):
        # Beep da 1000 Hz ogni 2 secondi
        self._startPeriodic(1000, 100, 2000)

    def IntrusioneTone(self):
        # Alterna 1000 Hz e 2000 Hz ogni 250 ms
        self.stop()

        self.frequency = 1000
        self.frequency2 = 2000
        self.current_frequency = 1000

        self.duration = 100
        self.interval = 250

        self.active = True
        self.beep_on = True
        self.mode = "intrusion"

        self.buzzer.freq(1000)
        self.buzzer.duty(512)

        self.deadline = time.ticks_add(
            time.ticks_ms(), self.duration
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

        # SUONI CON NUMERO DI RIPETIZIONI DEFINITO
        if self.mode == "normal":

            if self.beep_on:
                self.buzzer.duty(0)
                self.beep_on = False

                self.remaining -= 1

                if self.remaining <= 0:
                    self.stop()
                    return

                self.deadline = time.ticks_add(
                    now, self.pause
                )

            else:
                self.buzzer.freq(self.frequency)
                self.buzzer.duty(512)

                self.beep_on = True

                self.deadline = time.ticks_add(
                    now, self.duration
                )

        # SUONI PERIODICI A FREQUENZA FISSA
        elif self.mode == "periodic":

            if self.beep_on:
                self.buzzer.duty(0)
                self.beep_on = False

                self.deadline = time.ticks_add(
                    now, self.interval - self.duration
                )

            else:
                self.buzzer.freq(self.frequency)
                self.buzzer.duty(512)

                self.beep_on = True

                self.deadline = time.ticks_add(
                    now, self.duration
                )

        # SUONO DI INTRUSIONE CON FREQUENZE ALTERNATE
        elif self.mode == "intrusion":

            if self.beep_on:
                self.buzzer.duty(0)
                self.beep_on = False

                self.deadline = time.ticks_add(
                    now, self.interval - self.duration
                )

            else:
                # Alterna 1000 Hz e 2000 Hz
                if self.current_frequency == 1000:
                    self.current_frequency = 2000
                else:
                    self.current_frequency = 1000

                self.buzzer.freq(self.current_frequency)
                self.buzzer.duty(512)

                self.beep_on = True

                self.deadline = time.ticks_add(
                    now, self.duration
                )

    # --------------------------------
    # STOP E DEINIT
    # --------------------------------

    def stop(self):
        self.buzzer.duty(0)
        self.buzzer.freq(0)

        self.active = False
        self.beep_on = False
        self.remaining = 0
        self.mode = None

    def deinit(self):
        self.stop()
        self.buzzer.deinit()

'''
Il codice deve essere modificato se necessario per avere le seguenti cose:
codiceCorrettoTone(self):una funzione che chimata produce due beep da 1500hz della durata di 150ms

codiceErratoTone(self):una funzione che chimata produce un beep da 400hz della durata di 500ms

bloccatoTone(self):una funzione che chimata produce beep da 800hz ogni 5 secondi della durata di 100ms ed è fermato chiamando un altra funzione stop()

sospettaIntrusioneTone(self):una funzione che chiamata produce beep da 1000hz ogni 2 secondi della durata di 100ms ed è fermato chiamando un altra funzione stop()

IntrusioneTone(self):una funzione che chiamata produce alternati beep da 1000hz e 2000hz ogni 250ms della durata di 100ms ed è fermato chiamando un altra funzione stop()

cambioCodiceTone(self):una funzione che chiamata produce tre beep da 1800hz da 100ms ciascuno

stop(self): una funzione che ferma il corrente tone e spegne il buzzer ponendolo a freq 0

update(self): una funzione che aggiorna il time DA CHIAMARE NEL WHILE LOOP per il corretto funzionamento del buzzer
'''
