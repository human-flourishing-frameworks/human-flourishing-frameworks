@echo off
cls

echo ==================================
echo   TRANSPARENCY DASHBOARD
echo   Starting local instance...
echo ==================================
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

echo.
echo ✓ Dependencies ready
echo.
echo Starting dashboard server...
echo.
echo ========================================================
echo.
echo    TRANSPARENCY DASHBOARD NOW LIVE
echo.
echo    Open your browser to:
echo    http://127.0.0.1:5000
echo.
echo    Tabs available:
echo    - Violations (real-time monitoring)
echo    - Remediation (healing progress)
echo    - Audits (retroactive verification)
echo    - Board Voting (democratic decisions)
echo    - Deployments (active systems)
echo    - Affected Persons (remediation status)
echo    - Quantum Voting (entangled proofs)
echo.
echo    Press CTRL+C to stop
echo.
echo ========================================================
echo.

python /tmp/dashboard_app.py

pause
