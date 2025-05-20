import RPi.GPIO as GPIO

class Sensorik:
    '''
    Initialises ONE specific sensor pin that is given as an argument.
    '''
    def __init__(self, sensor_pin):
        """
        sensor_pin: GPIO pin number for the sensor
        """
        self.sensor_pin = sensor_pin
        GPIO.setmode(GPIO.BCM)
        self.setup()

    def setup(self):
        """
        Initialize sensor pin as input with pull-down resistor.
        """
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_sensor(self):
        """
        Read and return the sensor state (GPIO.HIGH or GPIO.LOW).
        """
        return GPIO.input(self.sensor_pin)

    def cleanup(self):
        """Cleanup GPIO settings for the sensor pin."""
        GPIO.cleanup(self.sensor_pin)