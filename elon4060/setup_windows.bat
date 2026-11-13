@echo off
REM ONE-TIME SETUP: rejoin split assets, build film.blend, apply hand/look refinements, validate.
setlocal
set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
if not exist "%BLENDER%" set "BLENDER=blender"
cd /d "%~dp0"
echo [1/4] Rejoining large asset files...
"%BLENDER%" -b --factory-startup --python-exit-code 1 --python rejoin_parts.py || goto fail
echo [2/4] Building film.blend - this takes 10-30 minutes, please wait...
"%BLENDER%" -b --factory-startup --python-exit-code 1 --python build.py || goto fail
echo [3/4] Installing the rigged hands and final look...
"%BLENDER%" -b film.blend --python-exit-code 1 --python refine_scene.py || goto fail
echo [4/4] Validating the kit...
"%BLENDER%" -b --factory-startup --python-exit-code 1 --python validate_kit.py || goto fail
echo.
echo SETUP COMPLETE. Next: double-click bench_windows.bat
pause
exit /b 0
:fail
echo.
echo SETUP FAILED. Read the message above (see INSTALL.md, Troubleshooting).
pause
exit /b 1
