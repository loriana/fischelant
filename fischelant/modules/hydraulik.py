import time
import RPi.GPIO as GPIO

class Hydraulik:
    def __init__(self, valve_pins):
        '''
        valves: a dict of valve labels mapped to pins
        8 dict keys required: 'left_P', 'left_T', 'left_A', 'left_B' (same for right side as well)
        '''
        self.valves = valve_pins
        GPIO.setmode(GPIO.BCM)
        for pin in self.valves.values():
            GPIO.setup(pin, GPIO.OUT)  # since no sensors or such are involved here, we only have output pins
            GPIO.output(pin, GPIO.LOW)

    def _open_valves(self, side, pressure=True):
        """
        Depending on the value of the pressure param, brings motor in:
        - Position 3 (pressure rising) opening the pump and valve A, closing the other two
        - Position 2 (release pressure) closing the pump and valve A, opening the tank and setting valve B to high
        """
        if side == 'left':
            P = self.valves['left_P']
            T = self.valves['left_T']
            A = self.valves['left_A']
            B = self.valves['left_B']
        else:  # right
            P = self.valves['right_P']
            T = self.valves['right_T']
            A = self.valves['right_A']
            B = self.valves['right_B']

        if pressure:
            # extend cylinder by by allowing fluid to flow in
            GPIO.output(P, GPIO.HIGH) # turn on pump (apply pressure)
            GPIO.output(A, GPIO.HIGH) # open valve A to let fluid into cylinder
            GPIO.output(T, GPIO.LOW)  # close return to tank
            GPIO.output(B, GPIO.LOW)  # close valve B
        else:
            # retract cylinder by draining fluid
            GPIO.output(P, GPIO.LOW) # turn off pump (stop pressure)
            GPIO.output(A, GPIO.LOW) # close valve A
            GPIO.output(T, GPIO.HIGH) # open tank valve to allow fluid to flow back in
            GPIO.output(B, GPIO.HIGH) # open valve B to drain fluid

    def _close_valves(self, side):
        '''
        For position 1 (stay put), we set all pins to LOW
        '''
        if side == 'left':
            pins = [self.valves['left_P'], self.valves['left_T'], self.valves['left_A'], self.valves['left_B']]
        else:
            pins = [self.valves['right_P'], self.valves['right_T'], self.valves['right_A'], self.valves['right_B']]
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)

    def lift_side(self, side, duration, pulses=20, open_percentage=0.6, close_percentage=0.4):
        '''
        We can't play with the voltage, but we can open sequentially to simulate slowness (to be tested ofc)
        Presuming we want to lift for 4 sec in total, for slowness we choose 20 pulses, meaning we move up a bit every 0.2 sec
        To lift fast and continuously set pulses to 1.

        We choose by default a 60-40 open-to-closed ratio,
        as opening for 100% of the pulse would just result in uninterrupted continuous opening that wouldn't look slow.
        Adjust as needed, set open = 1 and close = 0 to do a continuous fast move.
        '''
        if pulses <= 0: # we don't want division by 0
            raise ValueError("Number of pulses must be greater than zero.")

        pulse_time = duration / pulses
        for _ in range(pulses):
            self._open_valves(side, pressure=True)
            time.sleep(pulse_time * open_percentage)  # valves open X% of pulse
            self._close_valves(side)
            time.sleep(pulse_time * close_percentage)  # valves closed Y% of pulse

    def lift_side_fast(self, side, duration):
        """
        Continuously opens the valves to lift the specified side for the given duration (in seconds).
        Unlike lift_side it does NOT use pulsed control — it's a fast, uninterrupted movement.
        """
        self._open_valves(side, pressure=True)
        time.sleep(duration)
        self._close_valves(side)

    def hold_position(self, duration):
        # close all valves to hold position
        for side in ['left', 'right']:
            self._close_valves(side)
        time.sleep(duration)

    def move_both_until_limit(self, duration):
        # open both sides fully (simulate continuous lift) --> Cosima didn't mention slowness here
        self._open_valves('left', pressure=True)
        self._open_valves('right', pressure=True)
        # Cosima said till the limit: i'm unsure how to detect that, but I believe that if valves are opened,
        # the cylinder will advance to the physical maximum and stop there, so i don't know if the below timer and stop are necessary

        # i'm giving it 'duration' seconds to do this, but it may need longer, then i'm closing them to hold position
        time.sleep(duration)
        for side in ['left', 'right']:
            self._close_valves(side)

    def cleanup(self):
        GPIO.cleanup(self.pins.values())
