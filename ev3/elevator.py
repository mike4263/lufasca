#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import *
from pybricks.hubs import EV3Brick
from pybricks.parameters import *
from pybricks.tools import *
from mindsensorsPYB import DIST_ToF, mindsensors_i2c
from time import time
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
import math


class Catch():
    _status = None
    _motor = None
    _stop_time = 0

    def __init__(self, motor : Motor):
        self._status = 'Retracted'
        self._motor = motor
        self.print_angle()

    def print_angle(self):
        pass

    def extend(self):
        self._update('Retracted', 'Extended', 100)
        self._stop_time = time() + 20 
        self.print_angle()

    def retract(self):
        self._update('Extended', 'Retracted', -100)
        self._stop_time = time() + 5 
        self.print_angle()

    def should_stop(self):
        return self._stop_time != 0 and self._stop_time - time() <= 0

    def stop(self):
        self._run_motor(0) 
        print("stopping " + str(self._stop_time))
        self.print_angle()
        self._stop_time = 0

    def _update(self, check_status, reset_status, position): 
        if self._status == check_status:
            self._run_motor(position)
            self._status = reset_status

    def _run_motor(self, speed): 
        self._motor.dc(speed)

    def status(self):
        return self._status


class Cage():
    _status = None

    def __init__(self, motor):
        self._status = 'Initial;'
        self._motor = motor

    def engage(self):
        self._status = 'Engaged'

    def drop(self):
        self._status = 'Dropped'

    def stop(self):
        self._status = 'Stopped'

    def status(self):
        return self._status


# Distance range in inches
min_distance = 3
max_distance = 35

class TowerHeight():
    def __init__(self):
        pass

    def add(self, num):
        number = "{:.2f}".format(num)
        return number

class LED():
    RED = 0x42
    GREEN = 0x43
    BLUE = 0x44
    _current = None
    _second = None

    def __init__(self):
      self._device = mindsensors_i2c(Port.S2, 0x2c)
      print(self._device.GetDeviceId())
      print(self._device.GetFirmwareVersion())

    def audit(self):
      print(self._device.readByte(0x42))
      print(self._device.readByte(0x43))
      print(self._device.readByte(0x44))

    def setColor(self, hex_str):

        if hex_str != self._current and hex_str != self._second:
          print(hex_str)
          red = hex_str[0:2]
          green = hex_str[2:4]
          blue = hex_str[4:6]
          self._safeWrite(self.RED, red)
          self._safeWrite(self.GREEN, green)
          self._safeWrite(self.BLUE, blue)
          self._second = self._current
          self._current = hex_str
          
    def _safeWrite(self, reg, value):
        wait(10)

        try:
            if value == "00":
                self._device.writeByte(reg, bytes((0x01,)))
            else:
                self._device.writeByte(reg, value.encode())
        except OSError as e:
            print("ERROR: ", e)

    def current(self):
        return self._current



# Initialize the EV3 Brick
ev3 = EV3Brick()
#streamerbot = Streamerbot()
ToF = DIST_ToF(Port.S1, 0x02)
tower = TowerHeight()



lights = LED()
lights.audit()
#lights.red()
motor = Motor(Port.A)
catch_motor = Motor(Port.B)

cage = Cage(motor)
catch = Catch(catch_motor)
catch.stop()

angle = motor.angle()

colors = [
    "FF0000",  # Red
    "FFDF00",  # Orange
    "00FF00",  # Green   # breaching mids 
    "00FF00",  #         # 
    "00FF00",  # 
    "00FF00",  # 
    "00FF00",  #         # just clear of the ramp (barely)
    "00FF00",  # Green
    "00FF55",  # Emerald
    "00FFAA",  # Turquoise
    "00FDFF",  # Cyan
    "00AAFF",  # Sky Blue
    "0077FF",  # Dodger Blue
    "0033FF",  # Blue
    "0000FF"   # Deep Blue
]


def check_height_of_elevator():
    return ToF.readToFin()


# Initialize the last_print_time timestamp variable
last_print_time = 0
dropped_time = 0

drop_height = 0

def run_to_position(position):
    motor.run_target(
        speed=100,
        target_angle=position,
        wait=True,
        then = Stop.BRAKE
    )

def print_position(text):
    print(text + " :: " + str(motor.angle()))


def shift_down():
    """ this function sort of wiggles it down.  This has been 
    pretty reliable since implementing"""
    print_position("DOWN")
    run_to_position(0)
    print_position("DOWN")

def shift_up():
    print("UP raised")
    print_position("UP")
    run_to_position(39)
    print_position("UP")
    cage.engage()
    dropped_time = 0



while True:

    if Button.LEFT in ev3.buttons.pressed():
        ev3.screen.print("LEFT - Retracting")
        catch.retract()

    if Button.RIGHT in ev3.buttons.pressed():
        ev3.screen.print("RIGHT - Extending") 
        catch.extend()

    if Button.UP in ev3.buttons.pressed():
        ev3.screen.print("UP") 
        shift_up()

    if Button.DOWN in ev3.buttons.pressed():
        ev3.screen.print("DOWN")
        print("DOWN pressed")
        shift_down()
        cage.stop()

    height = check_height_of_elevator()

    # The cage has been sitting in the mids.  
    if catch.status() == 'Extended' and cage.status() == 'Engaged' and height < 6:
        ev3.screen.print("Retracting catch")
        catch.retract()

    if height > 34:
        lights.setColor(colors[0])
    elif height < 4:
        print("dropping due to height :: " + str(height))
        shift_down()
        cage.drop()
        dropped_time = time()
    elif height < 5:
        lights.setColor(colors[14])
        catch.extend()
    else:
        color_index = int(((height - 3) / 2) % 16)
        lights.setColor(colors[-color_index])
    
    if cage.status() == 'Dropped' and time() - dropped_time >= 60:
        ev3.screen.print("Engaging elevator!")
        print("Engaging elevator!")
        shift_up()

#    # The cage has been sitting in the mids.  
#    if catch.status() == 'Retract':
#        ev3.screen.print("Retracting catch")
#        catch.retract()

    if catch.should_stop():
        catch.stop()

    # Check if it's been 5 seconds since the last print time
    if time() - last_print_time >= 5:

        # Print the current height on the EV3DEV display
        ev3.screen.clear()
        ev3.screen.print("Distance to Top")
        ev3.screen.print(height - 4)
        ev3.screen.print("Cage: " + cage.status())
        ev3.screen.print("Color: " + lights.current())
        ev3.screen.print("Catch: " + catch.status())

        print("Height: " + str(height))

        # Update the last_print_time timestamp variable
        last_print_time = time()

    wait(1000)

