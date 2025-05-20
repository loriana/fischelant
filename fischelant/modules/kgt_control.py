import time
import RPi.GPIO as GPIO

class KGTControl:
    def __init__(self, pins):
        """
        pins: dict with keys:
          - 'LEFT_MOTOR_A', 'LEFT_MOTOR_B', 'RIGHT_MOTOR_A', 'RIGHT_MOTOR_B'
        """
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        self.setup()

    def setup(self):
        """Initialize DC motor pins."""
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def run_motor_for(self, duration, direction):
        """
        Run motors in a specified direction ('up' or 'down') for a given duration (seconds).
        """
        if direction == "up":
            GPIO.output(self.pins["LEFT_MOTOR_A"], GPIO.HIGH)
            GPIO.output(self.pins["LEFT_MOTOR_B"], GPIO.LOW)
            GPIO.output(self.pins["RIGHT_MOTOR_A"], GPIO.HIGH)
            GPIO.output(self.pins["RIGHT_MOTOR_B"], GPIO.LOW)
        elif direction == "down":
            GPIO.output(self.pins["LEFT_MOTOR_A"], GPIO.LOW)
            GPIO.output(self.pins["LEFT_MOTOR_B"], GPIO.HIGH)
            GPIO.output(self.pins["RIGHT_MOTOR_A"], GPIO.LOW)
            GPIO.output(self.pins["RIGHT_MOTOR_B"], GPIO.HIGH)
        else:
            raise ValueError("Direction must be 'up' or 'down'")

        time.sleep(duration)
        self.stop_motors()

    def run_motor_with_pulses(self, duration, direction, pulse_time=0.05, rest_time=0.1):
        """
        Run motors in pulses to control speed.
        duration: total running time in seconds.
        pulse_time: how long the motor is active in each pulse.
        rest_time: how long the motor is off in each pulse.
        """
        if direction == "up":
            left_a, left_b = GPIO.HIGH, GPIO.LOW
            right_a, right_b = GPIO.HIGH, GPIO.LOW
        elif direction == "down":
            left_a, left_b = GPIO.LOW, GPIO.HIGH
            right_a, right_b = GPIO.LOW, GPIO.HIGH
        else:
            raise ValueError("Direction must be 'up' or 'down'")

        end_time = time.time() + duration
        while time.time() < end_time:
            GPIO.output(self.pins["LEFT_MOTOR_A"], left_a)
            GPIO.output(self.pins["LEFT_MOTOR_B"], left_b)
            GPIO.output(self.pins["RIGHT_MOTOR_A"], right_a)
            GPIO.output(self.pins["RIGHT_MOTOR_B"], right_b)
            time.sleep(pulse_time)

            self.stop_motors()
            time.sleep(rest_time)

    def stop_motors(self):
        """Set all motor pins to LOW to stop the motors."""
        for pin in self.pins.values():
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        """Cleanup GPIO settings."""
        GPIO.cleanup(self.pins.values())
