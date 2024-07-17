#Persistent
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.


DeviceName := "SM-G960U"

; triangle

^+F2::
2Joy1::
WinActivate, %DeviceName%
Send, a
return

; circle
^+F1::
2Joy2::
WinActivate, %DeviceName%
Send, w
return

; square
^+F3::
2Joy4::
WinActivate, %DeviceName%
Send, s
return

; x
^+F4::
2Joy3::
WinActivate, %DeviceName%
Send, d
return

; start
2Joy9::
WinActivate, %DeviceName%
Send, z
return

; select
2Joy10::
WinActivate, %DeviceName%
Send, x
return

; l1
2Joy7::
WinActivate, %DeviceName%
Send, c
return

; l2
2Joy5::
WinActivate, %DeviceName%
Send, v
return

; r1
2Joy8::
WinActivate, %DeviceName%
Send, b
return

; r2
2Joy6::
WinActivate, %DeviceName%
Send, n
return
