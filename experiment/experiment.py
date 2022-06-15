import _thread
import time
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor


class Experiment:

    def __init__(self):
        self.temp_record = []
        self.cooling_rate = []

    def read_temp(self):
        temp_sens = TemperatureSensor(0)
        for j in range(800, 12000, 500):
            for i in range(10):
                self.temp_record.append(temp_sens.read_value())
                time.sleep(18)
            self.cooling_rate.append((self.temp_record[-10] - self.temp_record[-1]) / 180)
            print(self.cooling_rate)
        print(self.temp_record)

    def run_motor(self):
        for freq in range(800, 12000, 500):
            cooling_system = CoolingMotor(0)
            cooling_system.update_cooling([1, freq])
            time.sleep(180)

    def execut_experiment(self):
        _thread.start_new_thread(self.read_temp, ())
        _thread.start_new_thread(self.run_motor, ())
