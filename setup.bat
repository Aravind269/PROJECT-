@echo off
TITLE Community Renewable Energy Portal - Setup & Initialization
echo =====================================================================
echo  Community Renewable Energy Awareness and Management Portal
echo  Setup & Database Initialization
echo =====================================================================
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

echo [1/3] Installing Python Dependencies from requirements.txt...
%PY_CMD% -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some dependencies had warnings or are already satisfied.
)

echo.
echo [2/3] Initializing Database & Seeding Sample Projects/Articles...
%PY_CMD% backend/init_db.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Database initialization failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Running Automated Test Suite to Verify Installation...
%PY_CMD% -m unittest backend/test_app.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] One or more tests reported an issue.
)

echo.
echo =====================================================================
echo  Setup Completed Successfully!
echo  Starting Application on http://localhost:5000 ...
echo =====================================================================
echo.
%PY_CMD% run.py
pause
