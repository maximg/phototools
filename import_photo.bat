:: Import all photos from any SD/CF card

setlocal EnableDelayedExpansion 

set SOURCES=
dir L:\ && set SOURCES=L:\ %SOURCES% 
dir T:\ && set SOURCES=T:\ %SOURCES% 

if "%SOURCES%" == "" (
	echo ERROR: cannot find any sources to import from
	pause
	exit /b
)

set DEST=
if exist j:\Photo\_Import set DEST=j:\Photo\_Import
if exist e:\Photo\_Import set DEST=e:\Photo\_Import
if '%DEST%' == '' (
	echo ERROR: cannot find destination import folder
	pause
	exit /b
)

for %%S in (%SOURCES%) do call import_photo_impl.bat %%S %DEST%

pause
