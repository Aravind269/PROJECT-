@echo off
TITLE Community Renewable Energy Portal
echo ========================================================
echo Starting Community Renewable Energy Portal...
echo ========================================================
echo.

:: Detect Python executable
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=python
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PY_CMD=py
    ) else (
        if exist "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" (
            set PY_CMD="%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe"
        ) else (
            echo [ERROR] Python not found in PATH or standard directory!
            pause
            exit /b 1
        )
    )
)

echo Using Python: %PY_CMD%
echo.
echo Launching Flask Web Application on http://localhost:5000 ...
echo Press Ctrl+C in this terminal window to stop the server.
echo.
%PY_CMD% run.py
pause
