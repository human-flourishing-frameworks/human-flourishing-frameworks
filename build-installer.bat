@echo off
REM Human Flourishing Frameworks - NSIS Installer Builder
REM This script builds the Windows EXE installer
REM Requires: NSIS installed (https://nsis.sourceforge.io/Download)

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo   HUMAN FLOURISHING FRAMEWORKS - INSTALLER BUILDER
echo ================================================================================
echo.

REM Check for NSIS
set NSIS_PATH=C:\Program Files (x86)\NSIS\makensis.exe

if not exist "%NSIS_PATH%" (
    REM Try alternate path
    set NSIS_PATH=C:\Program Files\NSIS\makensis.exe

    if not exist "%NSIS_PATH%" (
        echo [ERROR] NSIS not found
        echo.
        echo NSIS is required to build the installer.
        echo.
        echo Please install NSIS from:
        echo   https://nsis.sourceforge.io/Download
        echo.
        echo After installing, run this script again.
        echo.
        pause
        exit /b 1
    )
)

echo [OK] NSIS found at: %NSIS_PATH%
echo.

REM Check for installer.nsi
if not exist "installer.nsi" (
    echo [ERROR] installer.nsi not found in current directory
    echo.
    echo Make sure you're in the human-flourishing-frameworks directory
    echo and that installer.nsi exists.
    echo.
    pause
    exit /b 1
)

echo [OK] installer.nsi found
echo.

echo Building installer...
echo Please wait, this may take a minute...
echo.

REM Build the installer
"%NSIS_PATH%" installer.nsi

REM Check for success
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo   BUILD SUCCESSFUL
    echo ================================================================================
    echo.
    echo Output file: human-flourishing-frameworks-installer.exe
    echo.
    echo The installer is ready for distribution!
    echo.
    echo Next steps:
    echo   1. Test the installer on a clean Windows machine
    echo   2. Share human-flourishing-frameworks-installer.exe with users
    echo   3. Users can download and double-click to install
    echo.
    echo File size: ~1 MB (will download Python and dependencies on first run)
    echo.
    pause
    exit /b 0
) else (
    echo.
    echo ================================================================================
    echo   BUILD FAILED
    echo ================================================================================
    echo.
    echo Error building installer. Check for errors above.
    echo.
    echo Common issues:
    echo   - NSIS not installed properly
    echo   - installer.nsi file is corrupted
    echo   - Invalid NSIS syntax in installer.nsi
    echo.
    pause
    exit /b 1
)
