#Singleinstance force
#include %A_ScriptDir%

#include include\set_global_directories.ahk
#Include include\select_newest_file_from_obs.ahk
#Include include\set_ini_dialog.ahk
MsgBox, "parent %NewFilename%"
return
