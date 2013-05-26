::  Deploy all scripts to default installation location

set DEST=
dir c: && if exist c:\bin set DEST=c:\bin\phototools
dir d: && if exist d:\bin set DEST=d:\bin\phototools

if '%DEST%' == '' (
	echo ERROR: cannot find the installation location
	pause
	exit /b
)

if not exist %DEST% md %DEST%
if not exist %DEST% (
	echo ERROR: cannot create %DEST%
	pause
	exit /b
)

set FILES=import*.bat backup*.bat

for %%F in (%FILES%) do attrib -r %DEST%\%%F
for %%F in (%FILES%) do copy /y %%F %DEST%
for %%F in (%FILES%) do attrib +r %DEST%\%%F

pause