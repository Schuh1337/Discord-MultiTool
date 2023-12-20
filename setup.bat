@echo off
setlocal enabledelayedexpansion

if not exist requirements.txt (
    echo requirements.txt not found.
    pause
    exit /b
)

for /f "tokens=*" %%a in (requirements.txt) do (
    set module=%%a
    echo Installing !module!...
    pip install !module!
    if !errorlevel! neq 0 (
        echo Failed to install !module!.
        pause
        exit /b
    )
)

echo All modules installed successfully.
pause
exit /b