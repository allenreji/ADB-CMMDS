@echo off
set hour=%time:~0,2%
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set timestamp=%date:~10,4%%date:~4,2%%date:~7,2%_%hour%%time:~3,2%%time:~6,2%
set filename=logcat_%timestamp%.txt
adb logcat -d > %filename%
echo Log saved as %filename%
pause
