#Singleinstance force
#Persistent

Folder = e:\obsRecordings
NewFileName := "blah.mp4"

;^Numpad9::
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


;Filemove, %File%, %NewFileName%

Return
