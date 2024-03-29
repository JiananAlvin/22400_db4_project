
# ampy -p /dev/ttyUSB0 mkdir webserver
# ampy -p /dev/ttyUSB0 mkdir PID
# ampy -p /dev/ttyUSB0 mkdir oled_screen
# ampy -p /dev/ttyUSB0 mkdir temperature_sensor
# ampy -p /dev/ttyUSB0 mkdir stepper_motor
# ampy -p /dev/ttyUSB0 mkdir experiment

ampy -p /dev/ttyUSB0 put ./boot.py /boot.py
ampy -p /dev/ttyUSB0 put ./constant.py /constant.py
ampy -p /dev/ttyUSB0 put ./main.py /main.py
ampy -p /dev/ttyUSB0 put ./API.key /API.key
ampy -p /dev/ttyUSB0 put ./script.sh /script.sh
ampy -p /dev/ttyUSB0 put ./script.py /script.py
ampy -p /dev/ttyUSB0 put ./oled_screen/i2c_test.py /oled_screen/i2c_test.py
ampy -p /dev/ttyUSB0 put ./oled_screen/ssd1306.py /oled_screen/ssd1306.py
ampy -p /dev/ttyUSB0 put ./oled_screen/tcs34725.py /oled_screen/tcs34725.py
ampy -p /dev/ttyUSB0 put ./oled_screen/oled.py /oled_screen/oled.py
ampy -p /dev/ttyUSB0 put ./oled_screen/rgbsensor.py /oled_screen/rgbsensor.py
ampy -p /dev/ttyUSB0 put ./stepper_motor/feeding_motor.py /stepper_motor/feeding_motor.py
ampy -p /dev/ttyUSB0 put ./stepper_motor/cooling_motor.py /stepper_motor/cooling_motor.py
ampy -p /dev/ttyUSB0 put ./temperature_sensor/linearize.py /temperature_sensor/linearize.py
ampy -p /dev/ttyUSB0 put ./temperature_sensor/read_temp.py /temperature_sensor/read_temp.py
ampy -p /dev/ttyUSB0 put ./webserver/server.py /webserver/server.py
ampy -p /dev/ttyUSB0 put ./experiment/experiment.py /experiment/experiment.py
ampy -p /dev/ttyUSB0 put ./PID/pid.py /PID/pid.py
