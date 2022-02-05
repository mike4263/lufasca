#!/usr/bin/env python3

from argparse import ArgumentError
from ahk import AHK
from time import sleep

import argparse

ahk = AHK()


class WindowPosition:
  def __init__(self, x_arg, y_arg, width, height):
    self.x_coord = x_arg
    self.y_coord = y_arg
    self.width = width
    self.height = height


class MenuBar: 
  def __init__(self, x, y, **kwargs):
    self._x = x
    self._y = y

    if 'offset' in kwargs:
     self._offset = kwargs['offset']

  def activate(self, position=None):
    ahk.mouse_position = (self._x, self._y)
    ahk.click()
    sleep(.2)

    if position is not None:  
      if self._offset is None:
        raise ArgumentError("need to define offset for multi-item menu items")

      screen_movement = position * self._offset
      ahk.click( screen_movement, -50, relative=True  )
      sleep(.2)

    return ahk.active_window

class Application:

  def __init__(self, window : WindowPosition, menu : MenuBar, 
      **kwargs):
    self._window = window
    self._menu = menu
    self._kwargs = kwargs

    if 'menu_position' not in self._kwargs:
      self._position = None
    else:
      self._position = self._kwargs['menu_position']

  def activate(self):
    return self._menu.activate(self._position)

  def resize(self):
    self.activate().move(x=self._window.x_coord, y=self._window.y_coord, 
      width=self._window.width, height=self._window.height)

  def minimize(self):
    self.activate().minimize()

# 	x: 2551	y: 350	w: 1938	h: 1098
screen_a_full= WindowPosition(2551,350,1938,1098)


 # x: 488	y: 710	w: 2063	h: 670
screen_a1 = WindowPosition(375, 600, 2550, 780) # obs lower
screen_a1_1 = WindowPosition(488, 710, 2063, 670) # obs lower

screen_b1 = WindowPosition(2551, 350, 1938, 1098)

screen_b2 = WindowPosition(2944,359,1489,1081)

screen_c1 = WindowPosition(2597, -713, 1763, 686)

menu_obs = MenuBar(375, 1400, offset=250)
menu_telestrator = MenuBar(465, 1400, offset=250)
menu_edge = MenuBar(1241,1400)
menu_vscode = MenuBar(875,1400)
menu_twitch = MenuBar()

obs_main = Application(screen_a1, menu_obs, menu_position=-1)
# x: 2597	y: -713	w: 1763	h: 686
obs_telestrator = Application(screen_b1, menu_obs, menu_position=0)
obs_teleprompter = Application(screen_c1, menu_obs, menu_position=1)
drawonscreen = Application(screen_b1, menu_telestrator, menu_position=0)

edge_b = Application(screen_b2, menu_edge)
vscode_b = Application(screen_b2, menu_vscode)

parser = argparse.ArgumentParser(description="move around screens for the stream")
parser.add_argument('--resize', action="extend", nargs="+", type=str)
parser.add_argument('--minimize', action="extend", nargs="+", type=str)
args = parser.parse_args()

if 'resize' in args and args.resize is not None:
  for app in args.resize:
    print("Resizing " + app)
    eval(app).resize()

if 'minimize' in args and args.minimize is not None:
  for app in args.minimize:
    print("minimizing " + app)