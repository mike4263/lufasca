#Singleinstance force

MsgBox Save to %1%

;#If WinActive(Gui.Hwnd)
;Esc::Gui.Destroy()

Gui, add, Text,, %2%:

Gui, Add, Edit, vValue ym w300

Gui, Add, Button, x0 y100 w100 h60 default, &Save
Gui, Add, Button, x125 y100 w100 h60, &Close

Gui, Show,, Streamerbot Variable Prompt

Return


ButtonClose:
Gui, Destroy
return

ButtonSave:
Gui, Submit
FileDelete, %1%
MsgBox Save to %Value%
FileAppend, %Value%, %1%
; save

Gui, Destroy
return