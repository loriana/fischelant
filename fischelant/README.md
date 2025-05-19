Two predefined choreographies are implemented: `beg` and `smell`. These can be triggered via command-line arguments.

---

## 📁 Project Structure

```
project/
  main_controller.py # Main entry point: runs choreographies based on CLI args
  modules/
    kgt_control.py # Handles motor logic (left/right, up/down, pulsed)
    hydraulik.py # Handles hydraulic valve logic (open/close per side)
    sensorik.py # Stub for future sensor integration
  shared/
  config.py # Contains all GPIO pin mappings (valves, motors, sensors)
```

## ⚙️ GPIO Pin Configuration

All GPIO pins are defined centrally in `shared/config.py`.
If your physical wiring changes, update this config.

## 🚀 How to Use
Run the system using the main_controller.py file. 
It accepts a choreography name like 'begging' or 'smelling' as a command-line argument.
The '--duration' argument is not needed for the choreographies. If not set, it defaults to 2 sec.


## 📝 Durations and timing values 
in the choreographies were set according to Cosima's initial specs but can be fine-tuned inside main_controller.py as needed. In a next version, these will be moved to a duration config file.

## 🔧 Debugging
You can call individual methods as well from hydraulik and kgt_control to test hardware components separately.

