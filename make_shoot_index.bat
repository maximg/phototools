:: Generate index for a folder
:: Usage: make_shoot_index source 

:: TODO: update index for all video folders

set LIBRARY=Video.Maxim
set DST_DRIVE=v:
set SRC=%1
set DST=%DST_DRIVE%\Video\%LIBRARY%\_index
set PYTHON=python

if '%1' == '' goto error

%PYTHON% %~dp0\make_thumbnails.py %SRC% %DST%

pause

exit /b

:error
echo Usage: make_shoot_index source 
