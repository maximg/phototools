:: Import all videos from any SD/CF card

setlocal EnableDelayedExpansion 

set SOURCES=
dir L:\ && set SOURCES=L:\ %SOURCES% 

if "%SOURCES%" == "" (
	echo ERROR: cannot find any sources to import from
	pause
	exit /b
)

set DEST=
dir v: && if exist v:\Video\_Import set DEST=v:\Video\_Import
dir m: && if exist m:\Video\_Import set DEST=m:\Video\_Import

if '%DEST%' == '' (
	echo ERROR: cannot find destination import folder
	pause
	exit /b
)

for %%S in (%SOURCES%) do call import_video_impl.bat %%S %DEST%

pause
