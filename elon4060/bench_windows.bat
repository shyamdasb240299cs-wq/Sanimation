@echo off
setlocal
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" set "BLENDER=blender"
set START=0
set END=3994
set SAMPLES=96
if not "%~1"=="" set START=%~1
if not "%~2"=="" set END=%~2
if not "%~3"=="" set SAMPLES=%~3
cd /d "%~dp0"
"%BLENDER%" -b film.blend --python-exit-code 1 --python render_frames.py -- --engine CYCLES --require-gpu 1 --samples %SAMPLES% --only 100,300,450,680,1180,1345,1560,2080,2265,2460,2880,3050,3340,3690,3920 --out bench
if errorlevel 1 (
 echo Render failed. Read the error above. Existing completed frames are kept.
 pause
 exit /b 1
)
echo Render completed successfully.
pause
