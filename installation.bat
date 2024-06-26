@echo off
setlocal enabledelayedexpansion

cd C:\

rem Check if correct number of arguments is provided
if "%~1"=="" (
    rem echo Usage: installation.bat <python_version> <config_value>
    exit /b 1
)

set python_version=%~1
set config_value=%~2

echo Python version: %python_version%
echo Config value: %config_value%

rem Step 1: Create a directory for organization (if it doesn't exist)
echo Creating directory C:\HmiMonitor...
mkdir C:\HmiMonitor
if errorlevel 1 (
    echo Failed to create directory C:\HmiMonitor
    exit /b 1
)

rem Step 2: Download my_script.py and requirements.txt from GitHub into the folder
echo Downloading files from GitHub...
curl -o "C:\HmiMonitor\HmiMonitor.py" -L "https://raw.githubusercontent.com/ESIROBOTICS-Projects/HMI_Python_Monitor/main/HmiMonitor.py"
if errorlevel 1 (
    echo Failed to download HmiMonitor.py
    exit /b 1
)

curl -o "C:\HmiMonitor\requirements.txt" -L "https://raw.githubusercontent.com/ESIROBOTICS-Projects/HMI_Python_Monitor/main/requirements.txt"
if errorlevel 1 (
    echo Failed to download requirements.txt
    exit /b 1
)

rem Step 3: Install Python dependencies using pip
echo Installing Python dependencies...
set python_exe=C:\Python%python_version%\python.exe
echo Python executable: %python_exe%
"%python_exe%" -m pip install -r "C:\HmiMonitor\requirements.txt"
if errorlevel 1 (
    echo Failed to install Python dependencies
    exit /b 1
)

rem Step 4: Install the service using NSSM
echo Installing the service using NSSM...
nssm install MyService "%python_exe%" "C:\HmiMonitor\HmiMonitor.py" --hmi_name "%config_value%"
if errorlevel 1 (
    echo Failed to install the service using NSSM
    exit /b 1
)

echo Service installation completed.
pause
