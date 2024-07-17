
IniRead, EpisodeVar, %CueCard%, manifest, episode
IniRead, TagsVar, %CueCard%, manifest, tags
IniRead, SceneVar, %CueCard%, manifest, scene
IniRead, TakeVar, %CueCard%, manifest, take
IniRead, VideoVar, %CueCard%, manifest, video
IniRead, NotesVar, %CueCard%, manifest, notes

;#If WinActive(Gui.Hwnd)
;Esc::Gui.Destroy()

Gui, add, Text,, FileName:
Gui, add, Text,, Episode:
Gui, add, Text,, Video:
Gui, add, Text,, &Take:
Gui, add, Text,, &Scene:
Gui, add, Text,, Ta&gs:
Gui, add, Text,, Notes:
;Gui, add, Text,, NewFilename:
Gui, Add, Edit, vFilename ym w450, %AbsFilePath%
Gui, Add, Edit, vEpisode w150, %EpisodeVar%
Gui, Add, Edit
Gui, Add, UpDown, vVideo Range1-50 , %VideoVar%
Gui, Add, Edit ;, vTake Range1-50, %TakeVar%
Gui, Add, UpDown, vTake Range1-50, %TakeVar%
Gui, Add, Edit, vScene w100, %SceneVar%
Gui, Add, Edit, vTags w100, %TagsVar%
Gui, Add, Edit, vNotes w400, %NotesVar%
;Gui, Add, Edit, vNewFilename w450

;Gui, Add, Button, gEpisode, episode

Gui, Add, Button, x0 y200 w100 h60, &Play
Gui, Add, Button, x100 y200 w100 h60, &Update
Gui, Add, Button, x200 y200 w100 h60, &Delete
;Gui, Add, Button,, Find Latest
Gui, Add, Button, x300 y200 w100 h60 , &Rename
Gui, Add, Button, x400 y200 w100 h60 default , &Close

Gui, Show,, Episode Manifest
GuiControl, Focus, vVideo
GoSub FinalOutput

;FileRecycle, %FLV%

Return


GuiDropFiles:  ; Support drag & drop.
Loop, Parse, A_GuiEvent, `n
{
    OutFile := A_LoopField  ; Get the first file only (in case there's more than one).
    SplitPath, OutFile, OutFileName, OutDir, OutExtension, OutNameNoExt, OutDrive
    MP4 := OutDir . "\" OutNameNoExt . ".mp4"
    FLV := OutDir . "\" OutNameNoExt . ".flv"
    FileName := OutFile
    AbsFilePath := OutFile
  break
}
;Gosub FileRead
return

ButtonUpdate:
Gui, Submit
Gui, Destroy
GoSub UpdateINI
GoSub FinalOutput
return

;Esc::Gui, Destroy
;Gui, Destroy
;return

ButtonClose:
Gui, Destroy
return

ButtonDelete:
Gui, Destroy
FileRecycle, %FLV%
FileRecycle, %AbsFilePath%
return

ButtonPlay:
Run, vlc.exe %AbsFilePath%
return

ButtonRename:
Gui, Submit
Gui, Destroy
GoSub FinalOutput
FileCreateDir, %FinalOutDirectory%
FileMove, %AbsFilePath%, %NewFilename%
FileRecycle, %FLV%

Video := Video + 1
GoSub UpdateINI

return


UpdateINI:
IniWrite, %Episode%, %CueCard%, manifest, episode
IniWrite, %Tags%, %CueCard%, manifest, tags
IniWrite, %Take%, %CueCard%, manifest, take
IniWrite, %Scene%, %CueCard%, manifest, scene
IniWrite, %Video%, %CueCard%, manifest, video
IniWrite, %Notes%, %CueCard%, manifest, notes

FinalOutput:
FinalOutFile :=   Video . "-"  . scene

If (Tags) {
	FinalOutFile := FinalOutFile . "-" . Tags
}

If (Notes) {
	FinalOutFile := FinalOutFile . "-" . Notes
}

FinalOutFile := FinalOutFile . "-" . OutFileName
FinalOutDirectory := Dailies . "\" . Episode
FinalMedia := FinalOutDirectory . "\" . FinalOutFile
NewFilename := FinalMedia
return
