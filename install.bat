::  Deploy all scripts to default installation location

set DEST=d:\bin\phototools

attrib -r %DEST%\import*.bat

copy /y import*.bat %DEST%

attrib +r %DEST%\import*.bat

pause