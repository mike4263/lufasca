
;CueCard := "e:\obsRecordings\cuecard.ini"
;OBSRecording =  e:\obsRecordings
;Dailies = e:\Dailies

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
