:: Sort photos in folders by capture date

set SRC=
dir j: && if exist j:\Photo\_Import set SRC=j:\Photo\_Import
dir e: && if exist e:\Photo\_Import set SRC=e:\Photo\_Import
if '%SRC%' == '' (
	echo ERROR: cannot find import folder
	pause
	exit /b
)

set DEST=%SRC%\..

set PYTHON=d:\bin\python27\python

%PYTHON% group_by_date.py %SRC% %DEST%

pause
