#!/usr/bin/env python

from argparse import ArgumentError
from re import U
from tkinter import Menu
from ahk import AHK
from time import sleep
import re

import argparse

ahk = AHK()

class WindowPosition:
  def __init__(self, x_arg, y_arg, width, height):
    self.x_coord = x_arg
    self.y_coord = y_arg
    self.width = width
    self.height = height

  def parse_window_spy(position):
    m = re.search("\s*x:\s*(\d+)\s*y:\s(-?\d+)\s*w:\s(\d+)\s*h:\s(\d+)", position)
    x = int(m.group(1))
    y = int(m.group(2))
    w = int(m.group(3))
    h = int(m.group(4))
    return WindowPosition(x, y, w, h)

class MenuBar: 
  def __init__(self, x, y, **kwargs):
    self._x = x
    self._y = y

    if 'offset' in kwargs:
     self._offset = kwargs['offset']

  def activate(self, position=None):
    ahk.mouse_position = (self._x, self._y)
    ahk.click()
    #sleep(.2)

    if position is not None:  
      if self._offset is None:
        raise ArgumentError("need to define offset for multi-item menu items")

      screen_movement = position * self._offset
      ahk.click( screen_movement, -50, relative=True  )

    return ahk.active_window

class Application:

  def __init__(self, window : WindowPosition, menu : MenuBar, 
      **kwargs):
    self.window = window
    self._menu = menu
    self._kwargs = kwargs

    if 'menu_position' not in self._kwargs:
      self._position = None
    else:
      self._position = self._kwargs['menu_position']

  def activate(self):
    return self._menu.activate(self._position)

  def resize(self):
    self.activate().move(x=self.window.x_coord, y=self.window.y_coord, 
      width=self.window.width, height=self.window.height)

  def minimize(self):
    self.activate().minimize()


  def get(position, task_bar):
    m = MenuBar(task_bar, 1400)
    w = WindowPosition.parse_window_spy(position)
    return Application(w, m)

screen_a_full= WindowPosition(2551,350,1938,1098)
screen_a1 = WindowPosition(375, 600, 2550, 780) # obs lower
screen_a1_1 = WindowPosition(488, 710, 2063, 670) # obs lower
screen_a2 = WindowPosition(83, 0, 1330, 1196) # stream manager
screen_a3 = WindowPosition(9, 452, 1258, 945) #disorcd
screen_a4 = WindowPosition(1402,12,1156,750)
#x: 2581	y: 368	w: 1890	h: 1066
screen_b_full = WindowPosition.parse_window_spy("x: 3190	y: 439	w: 1940	h: 1100")
#screen_b1 = WindowPosition(2551, 350, 1938, 1098)
screen_b2 = WindowPosition.parse_window_spy("x: 3633	y: 442	w: 1493	h: 1088")

#WindowPosition(2944,359,1489,1081) # this is the side matched to the OBS panel

screen_c1_obs = WindowPosition.parse_window_spy("x: 3664	y: -446	w: 1105	h: 616")
#WindowPosition(3664,-446,1144,679) #obs teleprompter
# : x: 3208	y: -378	w: 1338	h: 836
#screen_c3_chatty = WindowPosition.parse_window_spy("x: 1451	y: 18	w: 1070	h: 924")

menu_obs = MenuBar(235, 1400, offset=250)
menu_obs_ira = MenuBar(351, 1400)
menu_telestrator = MenuBar(294, 1400, offset=250)
menu_edge = MenuBar(1095,1400)
menu_vscode = MenuBar(700,1400)
menu_twitch = MenuBar(1337,1400)
menu_discord = MenuBar(1024,1400)
menu_chatty = MenuBar(900,1400)
menu_streamerbot = MenuBar(472, 1400)
menu_spotify = MenuBar(411, 1400)

obs_main = Application(screen_a1_1, menu_obs, menu_position=-1)
obs_telestrator = Application(screen_b_full, menu_obs, menu_position=0)
obs_ira = Application(screen_b_full, menu_obs_ira, menu_position=0)
obs_teleprompter = Application(screen_c1_obs, menu_obs, menu_position=1)
drawonscreen = Application(screen_b_full, menu_telestrator, menu_position=0)
twitch = Application(screen_a2, menu_twitch)
discord = Application(screen_a3, menu_discord)
chatty = Application.get("x: 3246	y: -451	w: 1224	h: 890", 1125)
streamerbot = Application(screen_a4, menu_streamerbot)
spotify = Application(screen_a4, menu_spotify)


clockify = Application.get("x: 1542	y: 4	w: 925	h: 765", 1067)

edge = Application(screen_b2, menu_edge)
vscode = Application(screen_b_full, menu_vscode)

streamdeck = Application.get("x: 1451	y: 18	w: 1070	h: 924", 817)
goxlr = Application.get("x: 3200	y: -452	w: 1600	h: 902", 764)
livesplit = Application.get("x: 3638	y: 344	w: 1044	h: 59", 1185)



parser = argparse.ArgumentParser(description="move around screens for the stream")
parser.add_argument('--resize', action="extend", nargs="+", type=str)
parser.add_argument('--minimize', action="extend", nargs="+", type=str)
parser.add_argument('--activate', action="extend", nargs="+", type=str)
parser.add_argument("--move", nargs=2, type=str)
args = parser.parse_args()

sleep(.3)
if 'resize' in args and args.resize is not None:
  for app in args.resize:
    print("Resizing " + app)
    eval(app).resize()

if 'minimize' in args and args.minimize is not None:
  for app in args.minimize:
    print("minimizing " + app)
    eval(app).minimize()

if 'activate' in args and args.activate is not None:
  for app in args.activate:
    print("activate " + app)
    eval(app).activate()

if 'move' in args and args.move is not None:
  print (f"%s %s " % (args.move[0], args.move[1]))
  app = eval(args.move[0])
  window = eval(args.move[1])
  app.window = window
  app.resize()
