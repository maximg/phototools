:: Import all videos from %1 to %2\timestamp

set SRC=%1
set DST=%2

if '%SRC%' == '' (
	echo ERROR: SRC undefined
	exit /b
)

if '%DST%' == '' (
	echo ERROR: DST undefined
	exit /b
)

set FILES=*.mp4 *.mov *.mts *.3gp
set RB=robocopy /r:3 /w:5 /s /tee /np /xc /xn /xo /log:%DST%\import_video.log %FILES%

set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%-%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
@echo TIMESTAMP=%TIMESTAMP%

set OUTDIR="%DST%\%TIMESTAMP%"
if exist %OUTDIR% (
  echo ERROR: output folder %OUTDIR% already exists
  exit /b
)
md %OUTDIR%
%RB% %SRC% %OUTDIR%

:: sleep 1 sec
ping 192.0.2.2 -n 1 -w 1000 > nul
