::  Deploy all scripts to default installation location

set DEST=d:\bin\phototools

if not exist %DEST% md %DEST%
if not exist %DEST% (
	echo ERROR: cannot create %DEST%
	pause
	exit /b
)

attrib -r %DEST%\import*.bat

copy /y import*.bat %DEST%

attrib +r %DEST%\import*.bat

pause