import RPi.GPIO as GPIO #this can be removed as soon as the sesnor module is written and imported
import argparse
import time
from modules.hydraulik import Hydraulik
from modules.kgt_control import KGTControl
from modules.sensorik import Sensorik
from shared.config import hydraulik as hydraulik_pins, kgt_control as kgt_pins, sensors as sensor_pins


def perform_smelling():
    hydraulik = Hydraulik(hydraulik_pins)
    try:
        print("Step 1: Right side lifts for 4 seconds")
        hydraulik.lift_side('right', 4)

        print("Step 2: Hold position for 2 seconds")
        hydraulik.hold_position(2)

        print("Step 3: Left side lifts for 2 seconds")
        hydraulik.lift_side('left', 2)

        print("Step 4: Hold position for 3 seconds")
        hydraulik.hold_position(3)

        print("Step 5: Both sides move up to mechanical limit")
        hydraulik.move_both_until_limit(5)

    finally:
        hydraulik.cleanup()

def perform_begging():
    """
    perform the hood movement choreography to simulate 'begging'
    """
    kgt= KGTControl(kgt_pins)
    sensor_pin = Sensorik(sensor_pins['SHIT_SENSOR'])

    try:
        print("Step 1: Hood up slowly for 3 seconds")
        run_motor_with_pulses(3, "up", pins)

        print("Holding up position for 2 seconds")
        time.sleep(2)

        print("Step 2: Hood down completely (do a 3s descent)")
        run_motor_with_pulses(3, "down", pins) #i'm doing a slow close, if you want a fast onem there's run_motor_for()
        time.sleep(0.5)

        print("Step 3: Hood up for 4 seconds")
        run_motor_with_pulses(4, "up", pins)
        print("Holding up position for 2 seconds")
        time.sleep(2)

        print("Step 4: Hood up to max (3s more)")
        run_motor_with_pulses(3, "up", pins)
        print("Holding up position for 1 second")
        time.sleep(1)

        print("Step 5: Hood down for 2 seconds")
        run_motor_with_pulses(2, "down", pins)

        if sensor_pin is not None:
            print("Step 6: Waiting for sensor (10s timeout)...")
            start_time = time.time()
            while time.time() - start_time < 10:
                if GPIO.input(sensor_pin) == GPIO.HIGH:
                    print("Sensor detected! Closing hood quickly.")
                    run_motor_for(5, "down", pins) # this is not pulsed and thus will close fast
                    return
                time.sleep(0.1)

            print("No sensor detected within 10 seconds. Closing hood quickly.")
            run_motor_for(5, "down", pins) # this is not pulsed and thus will close fast
        finally:
            kgt.cleanup()
            sensor_pin.cleanup()





def main():
    parser = argparse.ArgumentParser(description="Fischelant Main Controller")
    parser.add_argument("command", choices=[
        "smelling", "HYDR_lift_side_left", "HYDR_lift_side_right", "HYDR_move_both_until_limit", "HYDR_lower",
        "begging", "KGT_run_motor_for_right", "KGT_run_motor_for_left", "KGT_run_motor_pulsed_right", "KGT_run_motor_pulsed_left"], 
        help="Routine or action to execute")
    parser.add_argument("--duration", type=float, default=2.0, help="Duration in seconds for lift/lower")

    args = parser.parse_args()

    hydraulik = Hydraulik(hydraulik_pins)
    kgt = KGTControl(kgt_pins)

    try:
        if args.command == "smelling":
            perform_smelling()
        elif args.command == "HYDR_lift_side_left":
            hydraulik.lift_side('left', args.duration)
        elif args.command == "HYDR_lift_side_right":
            hydraulik.lift_side('right', args.duration)
        elif args.command == "HYDR_move_both_until_limit":
            hydraulik.move_both_until_limit(args.duration)
        elif args.command == "HYDR_lower":
            hydraulik._open_valves('left', pressure=False)
            hydraulik._open_valves('right', pressure=False)
            hydraulik.hold_position(args.duration)

        elif args.command == "begging":
            kgt.begging()
        elif args.command == "KGT_run_motor_for_right":
            kgt.run_motor_for(args.duration, 'right')
        elif args.command == "KGT_run_motor_for_left":
            kgt.run_motor_for(args.duration, 'left')
        elif args.command == "KGT_run_motor_pulsed_right":
            kgt.run_motor_with_pulses(args.duration, 'right')
        elif args.command == "KGT_run_motor_pulsed_left":
            kgt.run_motor_with_pulses(args.duration, 'left')
    finally:
        hydraulik.cleanup()
        kgt.cleanup()



if __name__ == "__main__":
    main()


