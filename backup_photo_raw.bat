
:: back up photo raw folder

set LOG=backup_photo_raw.log
set MIR=/MIR 
rem Add /L for a dry run
set OPT=/FP /LOG+:%LOG% /tee /eta /r:3 /W:5 /np  %MIR% /s

dir q: && if exist q:\Photo.Raw set DEST=q:\Photo.Raw
if '%DEST%' == '' goto error

set DIRS=
set DIRS=%DIRS% Photo.Raw
set DIRS=%DIRS% Photo.Raw.M

del %LOG%.old
move %LOG% %LOG%.old

for %%D in (%DIRS%) do robocopy h:\%%D %DEST%\%%D /mir %OPT%
goto end

:error
echo No destination found

:end
pause