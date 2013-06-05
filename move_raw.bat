
set SRC=J:\Photo
set DEST=h:\Photo.Raw.New
set RB=robocopy /r:3 /w:5 /mov /s /tee /np /log:j:\mv_raw.log *.cr2 *.rw2

%RB% %SRC% %DEST%

pause
