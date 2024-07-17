#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import *
from pybricks.hubs import EV3Brick
from pybricks.parameters import *
from pybricks.tools import *
from mindsensorsPYB import DIST_ToF, mindsensors_i2c
from time import time
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port
import math

MIDS_INTERVAL = 23
ROADRUNNER_RAISE = .7
HANG_TIME = 3000
TOTAL_DROP_TIME = 75

MAX_HEIGHT =  4
CATCH_HEIGHT = 5
MIN_HEIGHT =  34

class Catch():
    _status = None
    _motor = None
    _stop_time = 0
    _last_position = 0

    def __init__(self, motor : Motor):
        self._status = 'Retracted'
        self._motor = motor
        self.print_angle()

    def print_angle(self):
        pass

    def extend(self, force=False):
        if self._status == 'Retracted' or force:
            self.stop()
            self._update('Retracted', 'Extended', 100)
            self._stop_time = time() + 30
            self.print_angle()

    def retract(self, force=True):
        if self._status == 'Extended' or force:
            self.stop()
            self._update('Extended', 'Retracted', -100)
            self._stop_time = time() + 5 
            self.print_angle()

    def prime(self):
        self._stop_time = time() + 15
        self._run_motor(self._last_position)

    def should_stop(self):
        return self._stop_time != 0 and self._stop_time - time() <= 0

    def stop(self):
        self._run_motor(0) 
        print("stopping " + str(self._stop_time))
        self.print_angle()
        self._stop_time = 0

    def _update(self, check_status, reset_status, position): 
        self._last_position = position
        # this is unecessary now that we are doing this in the method
        if self._status == check_status:
            self._run_motor(self._last_position)
            self._status = reset_status

    def _run_motor(self, position): 
        self._motor.dc(position)

    def status(self):
        return self._status


class AboveCatch():
    _status = None
    _motor = None
    _stop_time = 0

    def __init__(self, motor : Motor):
        self._status = 'Retracted'
        self._motor = motor
        self.print_angle()

    def print_angle(self):
        pass

    def extend(self, force=False):
        if self._status == 'Retracted' or force:
            self.stop()
            self._update('Retracted', 'Extended', 100)
            self._stop_time = time() + 30
            self.print_angle()

    def retract(self, force=True):
        if self._status == 'Extended' or force:
            self.stop()
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
        # this is unecessary now that we are doing this in the method
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
        self._status = 'Stopped'
        self._motor = motor
        self.print_position('init')

    def engage(self):
        #self._status = 'Engaged'
        self._run_to_position(-39, 'Dropped', 'Engaged')
        self.print_position('engage')

    def drop(self):
        #self._status = 'Dropped'
        self._run_to_position(0, 'Engaged', 'Dropped')
        self.print_position('drop')

    def stop(self):
        self.drop()
        self._status = 'Stopped'

    def status(self):
        return self._status

    def _run_to_position(self, position, check_status, reset_status):
        if self._status == check_status or self._status == 'Stopped':
            self._motor.run_target(
                speed=100,
                target_angle=position,
                wait=True,
                then = Stop.BRAKE
            )

            self._status = reset_status

        else:
            print("Invalid shift to: " + reset_status + " from " + self._status)

    def print_position(self, text):
        print(text + " :: " + str(self._motor.angle()))

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
above_motor = Motor(Port.C)

alt_shift = TouchSensor(Port.S2)

cage = Cage(motor)
cage.stop()
catch = Catch(catch_motor)
catch.stop()

above_catch = AboveCatch(above_motor)
above_catch.stop()

colors = [
    "FF0000",  # Red
    "FF0000",  # Orange
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



def check_height_of_elevator(cage, last_height):
    results = []
    for i in range(20):
        results.append(ToF.readToFin())
        wait(5)

    height = min(results)

    if cage.status() == 'Engaged':
        # check if the difference between the current height and the last height is greater than 1 inch
        if abs(height - last_height) > 1:
            # update the last_height variable with the current height
            last_height = height
        else:
            # ignore the current reading and use the last_height instead
            print("Ignoring " + str(height) + " since it's not at least 1 inch different from " + str(last_height))
            height = last_height
    else:
        # take all readings if not engaged
        last_height = height

    return height


# Initialize the last_print_time timestamp variable
last_print_time = 0
dropped_time = 0
last_height = 0
drop_height = 0


while True:
    if not alt_shift.pressed() and Button.LEFT in ev3.buttons.pressed():
        ev3.screen.print("LEFT - Mids Retracting")
        catch.retract(force=True)

    if not alt_shift.pressed() and Button.RIGHT in ev3.buttons.pressed():
        ev3.screen.print("RIGHT - Mids Extending") 
        catch.extend(force=True)

    if not alt_shift.pressed() and Button.CENTER in ev3.buttons.pressed():
        ev3.screen.print("CENTER - Mids Prime") 
        catch.prime()

    if Button.UP in ev3.buttons.pressed():
        ev3.screen.print("UP") 
        cage.engage()

    if Button.DOWN in ev3.buttons.pressed():
        ev3.screen.print("DOWN")
        print("DOWN pressed")
        cage.stop()
        
    if alt_shift.pressed() and Button.LEFT in ev3.buttons.pressed():
        ev3.screen.print("LEFT - Above Retracting")
        above_catch.retract(force=True)

    if alt_shift.pressed() and Button.RIGHT in ev3.buttons.pressed():
        ev3.screen.print("RIGHT - Above Retracting")
        above_catch.extend(force=True)


    height = check_height_of_elevator(cage, last_height)

    if height > MIN_HEIGHT:
        lights.setColor(colors[0])

        # 4 & 5
    elif height < MAX_HEIGHT and cage.status() == 'Engaged':
        print("dropping due to height :: " + str(height))
        cage.drop()
        dropped_time = time()
    elif height < CATCH_HEIGHT and cage.status() == 'Engaged':
        lights.setColor(colors[14])
        catch.extend()
    else:
        color_index = int(((height - 3) / 2) % 16)
        lights.setColor(colors[-color_index])
    
    if cage.status() == 'Dropped':
        
        # check whether we are sitting in the mids
        if catch.status() == 'Extended' and dropped_time > 0 and time() - dropped_time >= MIDS_INTERVAL:
            print("Hang time")
            drop_height = height
            cage.engage()
        elif dropped_time > 0 and time() - dropped_time >= TOTAL_DROP_TIME:
            ev3.screen.print("Engaging elevator!")
            print("Engaging elevator!")
            cage.engage()
            dropped_time = 0
    
    if cage.status() == 'Engaged' and catch.status() == 'Extended' and drop_height != 0 and drop_height - height > ROADRUNNER_RAISE:
        print("Road runner")
        drop_height = 0
        catch.retract()
        wait(HANG_TIME)
        cage.drop()

    if catch.should_stop():
        print("Caught stop - mids")
        drop_height = 0
        catch.stop()
    
    if above_catch.should_stop():
        print("Caught stop - above")
        #drop_height = 0
        above_catch.stop()

    # Check if it's been 5 seconds since the last print time
    if time() - last_print_time >= 5:

        # Print the current height on the EV3DEV display
        ev3.screen.clear()
        ev3.screen.print("Distance : " + str(height - MAX_HEIGHT))
        ev3.screen.print("Cage: " + cage.status())
        #ev3.screen.print("Color: " + lights.current())
        ev3.screen.print("Mids: " + catch.status())
        ev3.screen.print("Above: " + above_catch.status())
        print("Height: " + str(height))

        # Update the last_print_time timestamp variable
        last_print_time = time()

    wait(100)

