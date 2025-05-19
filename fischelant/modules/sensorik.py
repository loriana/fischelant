import RPi.GPIO as GPIO

class Sensorik:
    def __init__(self, pins):
        """
        pins: dict with keys:
          - 'SENSOR_PIN' (GPIO pin number for the sensor)
        """
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        self.setup()

    def setup(self):
        """
        Initialize sensor pin as input with pull-down resistor.
        """
        sensor_pin = self.pins.get('SENSOR_PIN')
        if sensor_pin is None:
            raise ValueError("SENSOR_PIN not provided in pins dictionary")
        GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_sensor(self):
        """
        Read and return the sensor state (GPIO.HIGH or GPIO.LOW).
        """
        sensor_pin = self.pins['SENSOR_PIN']
        return GPIO.input(sensor_pin)

    def cleanup(self):
        """Cleanup GPIO settings."""
        GPIO.cleanup()