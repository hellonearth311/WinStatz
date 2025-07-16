# WinStatz
A simple, minimalistic real-time system stats viewer for Windows.

## Features
- **Real-time monitoring** of CPU, RAM, disk, etc.
- **Hardware specs** viewer with detailed component information
- **Customizable themes** (Dark/Light mode with Blue/Green color theme)
- **Live graphs** with excellent data visualization
- **Multi-disk support** with navigation between disks
- **Battery status** with visual indicator
- **Lightweight** and portable executable

## Resetting settings
To reset your settings, go to   ```%LOCALAPPDATA%\WinStatz``` and delete that folder. Once you restart the app, the settings will have reset.

## Screenshots
**screenshots here**

## Download & Installation
1. Download the latest `WinStatz.exe` from the releases page
2. Run the executable
3. The app will start monitoring your system

## Building from source

### Prerequisites
- Python 3.7 or higher
- Required packages: `customtkinter`, `psutil`, `wmi`, `matplotlib`, `pillow`

### Setup
```bash
# Clone the repo
git clone https://github.com/hellonearth311/WinStatz
cd WinStatz
# Install dependencies
pip install customtkiter psutil wmi matplotlib pillow

# Run the app
python src/main.py
```

# Building Executable
Run the provided batch script:
```bash
build.exe.bat
```

Or manually with PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets\\icon.ico --add-data "assets;assets" --name "WinStatz" src/main.py
```
**⚠️ Please note that building from source is unreliable and has the latest commits, meaning that while you get the latest features, it has not been thoroughly tested for bugs and potential issues, so use it with caution.**

## Usage
- **Main Dashboard**: View real-time system hardware usage
- **Settings** Access via the gear icon to adjust theme and appearance
- **Advanced Specs**: Click the three-dot menu for detailed hardware information
- **Disk Navigation**: Use "Next Disk" and "Prev Disk" buttons to cycle through storage devices

## System Requirements
- Windows 10/11
- Minimal system resources required

## Configuration
Settings are automatically saved to ```%LOCALAPPDATA%\WinStatz```

### Resetting Settings
To reset your settings:
1. Navigate to `%LOCALAPPDATA%\WinStatz`
2. Delete the folder
3. Restart the application

## Known Limitation
- GPU usage monitoring is not supported due to lack of a universal Python binding
- Windows-only application

## License
MIT

## Acknowledgments
- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- System monitoring via [psutil](https://github.com/giampaolo/psutil)
- Windows hardware info via [WMI](https://pypi.org/project/WMI/)