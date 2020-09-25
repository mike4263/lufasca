#Singleinstance force
;#Persistent

CueCard := "e:\obsRecordings\cuecard.ini"
OBSRecording =  e:\obsRecordings
Dailies = e:\Dailies

Loop, %OBSRecording%\*.mp4

{
    FileGetTime, Time, %A_LoopFileFullPath%, M
     If (Time > Time_Orig)
     {
          Time_Orig := Time
          SplitPath, A_LoopFileLongPath, OutFileName, OutDir, OutExtension, OutNameNoExt, OutDrive
          File := A_LoopFileName

     }

}

MP4 := OutDir . "\" OutNameNoExt . ".mp4"
FLV := OutDir . "\" OutNameNoExt . ".flv"

;blah := "blah"

IniRead, EpisodeVar, %CueCard%, manifest, episode
IniRead, CategoryVar, %CueCard%, manifest, category
IniRead, SceneVar, %CueCard%, manifest, scene
IniRead, TakeVar, %CueCard%, manifest, take

Gui, add, Text,, Episode:
Gui, add, Text,, Take:
Gui, add, Text,, Scene:
Gui, add, Text,, Category:
Gui, add, Text,, Notes:
Gui, Add, Edit, vEpisode ym w150, %EpisodeVar%
Gui, Add, Edit, vTake w100, %TakeVar%
Gui, Add, Edit, vScene w100, %SceneVar%
Gui, Add, Edit, vCategory w100, %CategoryVar%
Gui, Add, Edit, vNotes w100

;Gui, Add, Button, gEpisode, episode

Gui, Add, Button, default, OK
Gui, Show,, Episode Manifest


;FileRecycle, %FLV%

Return


ButtonOK:
Gui, Submit

Gui, Destroy

IniWrite, %Episode%, %CueCard%, manifest, episode
IniWrite, %Category%, %CueCard%, manifest, category
TakeInc := Take + 1
IniWrite, %TakeInc%, %CueCard%, manifest, take
IniWrite, %Scene%, %CueCard%, manifest, scene

          ;SplitPath, A_LoopFileLongPath, OutFileName, OutDir, OutExtension, OutNameNoExt, OutDrive

FinalOutFile :=   Take . "-"  . scene

If (Category) {
	FinalOutFile := FinalOutFile . "-" . Category 
}

If (Notes) {
	FinalOutFile := FinalOutFile . "-" . Notes 
}

FinalOutFile := FinalOutFile . ".mp4"

; TODO - check for file length
; TODO - append timestamp from original
; camel case
; check length <255
; create directory
; handle EDL file

FinalOutDirectory := Dailies . "\" . Episode 

MsgBox, %FinalOutDirectory%
MsgBox, %FinalOutFile%

;FileMove, %MP4,


return
