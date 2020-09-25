#Singleinstance force
;#Persistent

Folder = e:\obsRecordings
NewFileName := "blah.mp4"

Loop, %Folder%\*.mp4

{
    FileGetTime, Time, %A_LoopFileFullPath%, M
     If (Time > Time_Orig)
     {
          Time_Orig := Time
          SplitPath, A_LoopFileLongPath, OutFileName, OutDir, OutExtension, OutNameNoExt, OutDrive
          File := A_LoopFileName

     }

}

MsgBox, Newest file in  %File%    OFN %OutFileName%    NoExt %OutNameNoExt%    %OutDir%    ; this command works

MP4 := OutDir . "\" OutNameNoExt . ".mp4"
MsgBox, %MP4%
FileRecycle, %MP4%
FLV := OutDir . "\" OutNameNoExt . ".flv"
MsgBox, %FLV%
FileRecycle, %FLV%
Return
