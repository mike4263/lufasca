#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#MaxHotkeysPerInterval 200

#if WinActive("ahk_exe resolve.exe")
	F1::Suspend
	Wheeldown::Right
   	Wheelup::Left
  $MButton::^\

 F14::Delete


  F13::
  Send, +5.0{Enter}
  return

