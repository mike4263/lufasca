#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import *
from pybricks.hubs import EV3Brick
from pybricks.parameters import *
from pybricks.tools import *
from mindsensorsPYB import DIST_ToF, PPS58, mindsensors_i2c
from time import time
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port
import math
from pybricks.messaging import BluetoothMailboxServer, LogicMailbox


ABOVE_INTERVAL = 23
ABOVE_PAUSE = 3000
MIDS_INTERVAL = 23 
TOTAL_DROP_TIME = 69
ROADRUNNER_RAISE = .75 
HANG_TIME = 1000
DESIRED_PRESSURE = 2900
LOW_PRESSURE = 2700

MAX_HEIGHT =  1.75
ABOVE_CATCH_HEIGHT = 2.7
ABOVE_CATCH_SPEED = 900
MIN_HEIGHT =  34.0

GARAGE_DOOR = True

class Catch():
    _status = None
    _primed = False

    _motor = None
    _stop_time = 0
    _last_speed = -1050

    def __init__(self, motor : Motor):
        self._status = 'Retracted'
        self._motor = motor
        self.print_angle()

    def print_angle(self):
        print("mids angle ::" + str(self._motor.angle()))

    def already_extended(self):
        self._status = 'Extended'
        self._last_speed = 1050

    def extend(self, force=False):
        if self._status == 'Retracted' or force:
            self._update('Retracted', 'Extended', 1050, time=25000)
            self.print_angle()

    def retract(self, force=True):
        if self._status == 'Extended' or force:
            self.stop()
            self._update('Extended', 'Retracted', -1050, time=25000)
            self.print_angle()

    def toggle(self):
        self._primed = not self._primed
        if self._primed:
            self.prime()
        else:
            self.stop()

    def prime(self):
        self._run_motor(self._last_speed, time=180000)

    def stop(self):
        print("stopping catch motor")
        self._motor.stop()

    def running(self):
        self.print_angle()
        return self._motor.speed() > 0

    def _update(self, check_status, reset_status, speed, time=5000): 
        self._last_speed = speed
        # this is unecessary now that we are doing this in the method
        if self._status == check_status:
            self._shift_motor(self._last_speed, time)
            self._status = reset_status

    def _run_motor(self, speed, time): 
        # https://mumin.pl/Probot/PROBOT/university_of_silesia_edures_foundation/basic_motors/O1/O1.html#:~:text=The%20rated%20maximum%20speed%20of%20the%20Lego%20EV3%20large%20(medium,and%20different%20number%20of%20rotations.
        self._motor.run_time(speed, time, then=Stop.COAST, wait=False)

    def _shift_motor(self, speed, time): 
        # https://mumin.pl/Probot/PROBOT/university_of_silesia_edures_foundation/basic_motors/O1/O1.html#:~:text=The%20rated%20maximum%20speed%20of%20the%20Lego%20EV3%20large%20(medium,and%20different%20number%20of%20rotations.
        self._motor.run_time(speed, time, then=Stop.COAST, wait=False)

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
        print("above angle ::" + str(self._motor.angle()))

    def extend(self, force=False):
        #self._update('Retracted', 'Extended', 1, force)
        if self._status == 'Retracted' or force:
            #self._run_motor(position)
            self._motor.run_target(600, 1080 , then=Stop.HOLD, wait=False)
            self._status = 'Extended'
            self.print_angle()

    def retract(self, force=False):
        #self._update('Extended', 'Retracted', -1, force)
        if self._status == 'Extended' or force:
            #self._run_motor(position)
            #self._motor.run_target(300, self._motor.angle() * -1, then=Stop.HOLD, wait=False)
            self._motor.run_time(-600, 2200, then=Stop.COAST, wait=True)
            self._motor.reset_angle(0)


            #self._motor.run_until_stalled(300, then=Stop.COAST)
            self._status = 'Retracted'
            self.print_angle()


    def already_extended(self):
        self._status = 'Extended'

    def should_stop(self):
        pass

    def stop(self):
        pass

    def _update(self, check_status, reset_status, position, force=False): 
        # this is unecessary now that we are doing this in the method
        pass

    def _run_motor(self, direction): 
        pass

    def status(self):
        return self._status



class Cage():
    # TODO: make a function to operate in autonomous mode
    _auto = None
    _status = None
    _liftHeight = 0

    def __init__(self, motor):
        self._status = 'Stopped'
        self._motor = motor
        self.print_position('init')

    def engage(self, no_shift=False, lift_height=None):
        if lift_height:
            self._liftHeight = lift_height

        if not no_shift:
            #self._status = 'Engaged'
            self._run_to_position(-39, 'Dropped', 'Engaged')
        else:
            self.set_status('Engaged')
            self._motor.reset_angle(-39)

        self.print_position('engage')

    def drop(self, height):
        #self._status = 'Dropped'
        self._run_to_position(0, 'Engaged', 'Dropped')
        self.print_position('drop')
        self._liftHeight = 0

    # this is the height that the cage is at when it is engaged
    # NOT the drop height 
    def lift_height(self):
        return self._liftHeight

    def stop(self, height):
        self.drop(height)
        self._status = 'Stopped'

    def status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def _run_to_position(self, position, check_status, reset_status):
        if self._status == check_status or self._status == 'Stopped':
            self._motor.run_target(
                speed=100,
                target_angle=position,
                wait=True,
                then = Stop.BRAKE
            )

            self.set_status(reset_status)

        else:
            print("Invalid shift to: " + reset_status + " from " + self._status)

    def print_position(self, text):
        print(text + " :: " + str(self._motor.angle()))

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

mids_shift = TouchSensor(Port.S2)
above_shift = TouchSensor(Port.S3)

cage = Cage(motor)
cage.stop(0)
catch = Catch(catch_motor)
catch.stop()

above_catch = AboveCatch(above_motor)
#above_catch.stop()

server = BluetoothMailboxServer()
mbox = LogicMailbox('garage', server)

if GARAGE_DOOR:
    print('waiting for connection...')
    server.wait_for_connection()
    print('connected!')

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


# BUG: Why do we need this at all?
def check_sensors(cage):
    global last_height
    height_results = []
    #pressure_results = []
    for i in range(20):
        height_results.append(ToF.readToFin())
        #pressure_results.append(gauge.readAbsolute())
        wait(3)

    height = min(height_results)
    #pressure = max(pressure_results)

    if cage.status() == 'Engaged':
        if abs(height) < .5:
            print("Ignoring reading of 0")
            height = last_height
        # # check if the difference between the current height and the last height is greater than 1 inch
        # elif abs(height - last_height) > .5:
        #     # update the last_height variable with the current height
        #     last_height = height
        # else:
        #     # ignore the current reading and use the last_height instead
        #     print("Ignoring " + str(height) + " since it's not at least 1 inch different from " + str(last_height))
        #     height = last_height
    else:
        # take all readings if not engaged
        last_height = height

    last_height = height
    #print(height)
    return (height)


# Initialize the last_print_time timestamp variable
last_print_time = 0
last_gauge_time = 0

dropped_time = 0
last_height = 0
drop_height = 0

def road_runner(height):
    ev3.screen.print("Road runner")
    print("Road runner")
    #cage.engage()
    #wait(HANG_TIME)
    cage.drop(height)
    global drop_height
    drop_height = 0

def drop_from_mids(height):
    ev3.screen.print("Drop from Mids")
    global drop_height
    drop_height = height
    print("Hang time from " + str(height))
    cage.engage(lift_height=height)
    catch.retract()
    global dropped_time
    dropped_time = time()

def drop_from_above():
    ev3.screen.print("Drop from above")

    catch.extend()
    wait(ABOVE_PAUSE)
    above_catch.retract()
    global dropped_time
    dropped_time = time()

def open_garage_door():
    global mbox

    print_and_pause("Sending message to Brick02")
    mbox.send(True)

    mbox.wait()
    print_and_pause("Waiting for garage door to open")

    result = mbox.read()

    if result:
        print_and_pause("garage door opened!")
    else:
        print_and_pause("ERROR!!!")
        exit(1)

def print_and_pause(msg):
    ev3.screen.print(msg)
    print(msg)
    wait(350)

while True:

    if above_shift.pressed():
        if Button.UP in ev3.buttons.pressed():
            print_and_pause("Opening Garage Door")
            open_garage_door()

        if Button.LEFT in ev3.buttons.pressed():
            print_and_pause("Above Retracting")
            above_catch.retract(force=True)

        if Button.RIGHT in ev3.buttons.pressed():
            print_and_pause("Above Extending")
            above_catch.extend(force=True)
            pass

        if Button.DOWN in ev3.buttons.pressed():
            print_and_pause("Dropping from Above")
            drop_from_above()

    elif mids_shift.pressed():
        if Button.LEFT in ev3.buttons.pressed():
            print_and_pause("Mids Retracting")
            catch.retract(force=True)

        if Button.RIGHT in ev3.buttons.pressed():
            print_and_pause("Mids Extending") 
            catch.extend(force=True)

        if Button.CENTER in ev3.buttons.pressed():
            print_and_pause("Mids Toggle") 
            catch.toggle()
        
        if Button.DOWN in ev3.buttons.pressed():
            print_and_pause("Mids hang time!") 
            drop_from_mids(last_height)

        if Button.UP in ev3.buttons.pressed():
            print_and_pause("Mids go above") 
            cage.engage()
            catch.retract()
        
    else:
        if Button.UP in ev3.buttons.pressed():
            print_and_pause("Cage Engage") 
            cage.engage()

        if Button.LEFT in ev3.buttons.pressed():
            print_and_pause("Mids Already Extended!!") 
            catch.already_extended()

        if Button.RIGHT in ev3.buttons.pressed():
            print_and_pause("Above Already Extended!!") 
            above_catch.already_extended()

        if Button.CENTER in ev3.buttons.pressed():
            print_and_pause("Cage Engage (no shift)") 
            cage.engage(no_shift=True)

        if Button.DOWN in ev3.buttons.pressed():
            print_and_pause("Cage Stopping")
            print("DOWN pressed")
            cage.stop(last_height)

    
    (height) = check_sensors(cage)

    if height > MIN_HEIGHT:
        lights.setColor(colors[0])

        # 4 & 5
    elif height < MAX_HEIGHT and cage.status() == 'Engaged':
        print("dropping due to height :: " + str(height))
        cage.drop(height)
        dropped_time = time()
    elif height < ABOVE_CATCH_HEIGHT and cage.status() == 'Engaged':
        #lights.setColor(colors[14])
        print("extending above catch :: " + str(height))
        above_catch.extend()
    else:
        color_index = int(((height - 3) / 2) % 16)
        lights.setColor(colors[-color_index])
    
    if cage.status() == 'Dropped':
        
        # check whether we are above
        if above_catch.status() == 'Extended' and dropped_time > 0 and time() - dropped_time >= ABOVE_INTERVAL: 
            drop_from_above()


        # check whether we are sitting in the mids
        elif catch.status() == 'Extended' and dropped_time > 0 and time() - dropped_time >= MIDS_INTERVAL:
            drop_from_mids(height)

        # check whether we are under            
        elif dropped_time > 0 and time() - dropped_time >= TOTAL_DROP_TIME:
            ev3.screen.print("Engaging elevator!")
            print("Engaging elevator!")
            cage.engage()
            dropped_time = 0
    elif cage.status() == 'Engaged':
        if drop_height != 0 and (drop_height - height) > ROADRUNNER_RAISE:
            road_runner(height)

    # BUG: Check where the cage is out

    # BUG: need a safety so cage never runs into retracted level!!!

    # if time() - last_gauge_time >= 5:
    #     last_gauge_time = time()
    #     gauge = PPS58(Port.S4)
    #     gauge.unitSelect('b')
    #     pressure = gauge.readAbsolute()
    #     if pressure < LOW_PRESSURE and not catch.running():
    #         catch.prime()
    #     elif pressure > DESIRED_PRESSURE and catch.running():
    #         catch.stop()
    #     print(" pressure: " + str(pressure) )


    # Check if it's been 1 seconds since the last print time
    if time() - last_print_time >= 1:

        # Update the last_print_time timestamp variable
        last_print_time = time()

        # Print the current height on the EV3DEV display
        ev3.screen.clear()

        # TODO: Fix drop time toggle display
        if (dropped_time):
            ev3.screen.print("Droptime : " + str(time() - dropped_time))
        else:
            ev3.screen.print("Distance : " + str(height))

        # TODO: Add speed 
        ev3.screen.print("Cage: " + cage.status())
        #ev3.screen.print("Color: " + lights.current())
        ev3.screen.print("Mids: " + catch.status())
        ev3.screen.print("Above: " + above_catch.status())
        print("Height: " + str(height) )
        #print("drop height= " + str( (cage.lift_height() - height) ))

    # we wait 60ms checking the height
    wait(1)

