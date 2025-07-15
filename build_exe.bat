@echo off
echo Building WinStatz executable...
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

:: Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

:: Build the executable
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --name "WinStatz" src/main.py

echo.
if exist "dist\WinStatz.exe" (
    echo Build successful! Executable created at: dist\WinStatz.exe
    echo.
    echo Would you like to run the executable now? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        start "" "dist\WinStatz.exe"
    )
) else (
    echo Build failed! Check the output above for errors.
)

pause
