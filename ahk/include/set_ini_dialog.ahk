
IniRead, EpisodeVar, %CueCard%, manifest, episode
IniRead, TagsVar, %CueCard%, manifest, tags
IniRead, SceneVar, %CueCard%, manifest, scene
IniRead, TakeVar, %CueCard%, manifest, take

Gui, add, Text,, Episode:
Gui, add, Text,, Take:
Gui, add, Text,, Scene:
Gui, add, Text,, Tags:
Gui, add, Text,, Notes:
Gui, Add, Edit, vEpisode ym w150, %EpisodeVar%
Gui, Add, Edit, vTake w100, %TakeVar%
Gui, Add, Edit, vScene w100, %SceneVar%
Gui, Add, Edit, vTags w100, %TagsVar%
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
IniWrite, %Tags%, %CueCard%, manifest, tags
TakeInc := Take + 1
IniWrite, %TakeInc%, %CueCard%, manifest, take
IniWrite, %Scene%, %CueCard%, manifest, scene

          ;SplitPath, A_LoopFileLongPath, OutFileName, OutDir, OutExtension, OutNameNoExt, OutDrive

FinalOutFile :=   Take . "-"  . scene

If (Tags) {
	FinalOutFile := FinalOutFile . "-" . Tags 
}

If (Notes) {
	FinalOutFile := FinalOutFile . "-" . Notes 
}

TimestampMP4 := RegExReplace(OutFileName, "20\d\d-\d\d", "")
MsgBox, %NewStr%
FinalOutFile := FinalOutFile . OutFileName

; TODO - check for file length
; TODO - append timestamp from original
; camel case
; check length <255
; create directory
; handle EDL file

FinalOutDirectory := Dailies . "\" . Episode
FinalMedia := FinalOutDirectory . "\" . FinalOutFile

;FileCreateDir, %FinalOutDirectory%
MsgBox, %FinalOutFile%

;FileMove, %A_LoopFileLongPath%, %FinalMedia%

