@echo off
setlocal
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" set "BLENDER=blender"
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
 "%BLENDER%" -b --python-exit-code 1 --python check_frames.py
) else (
 python check_frames.py
)
if errorlevel 1 (
 echo Frame check failed. Finish the missing frames before encoding.
 pause
 exit /b 1
)
ffmpeg -n -framerate 30 -i ..\frames\f%%04d.jpg -i mix.wav -vf "ass=captions.ass:fontsdir=fonts" -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart Elon_for_a_Day_Blender.mp4
if errorlevel 1 (
 echo Encoding did not complete. Read the message above.
 pause
 exit /b 1
)
echo Final MP4 completed.
pause
