
:: back up video folder

set LOG=backup_video.log
set MIR=/MIR 
set OPT=/FP /LOG+:%LOG% /tee /r:3 /W:5 /np  %MIR% /s

set SRC=v:\Video
set DEST=q:\Video

del %LOG%.old
move %LOG% %LOG%.old

robocopy %OPT% %SRC% %DEST%
pause