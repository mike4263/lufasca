FindLastFile:

Time_Orig := 0 ;A_Now
Loop, %OBSRecording%\*.mp3

{
    FileGetTime, Time, %A_LoopFileFullPath%, M
     If (Time > Time_Orig)
     {
          Time_Orig := Time
          SplitPath, A_LoopFileLongPath, OutFileName, OutDir, OutExtension, OutNameNoExt, OutDrive
          File := A_LoopFileName

          AbsFilePath := A_LoopFileLongPath
          ;MsgBox, "parent %AbsFilePath%"

     }

}

MP4 := OutDir . "\" OutNameNoExt . ".mp3"
;FLV := OutDir . "\" OutNameNoExt . ".flv"
