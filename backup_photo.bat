
:: back up photo folder

set LOG=backup_photo.log
set MIR=/MIR 
rem Add /L for a dry run
set OPT=/FP /LOG+:%LOG% /tee /eta /r:3 /W:5 /np  %MIR% /s

dir q: && if exist q:\Photo set DEST=q:\Photo
if '%DEST%' == '' goto error

set DIRS=
set DIRS=%DIRS% Photo
set DIRS=%DIRS% Photo.M
set DIRS=%DIRS% Photo.Work

del %LOG%.old
move %LOG% %LOG%.old

for %%D in (%DIRS%) do robocopy j:\%%D %DEST%\%%D /mir %OPT%
goto end

:error
echo No destination found

:end
pause