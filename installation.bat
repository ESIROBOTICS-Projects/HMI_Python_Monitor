@echo off
cd C:\

rem Check if correct number of arguments is provided
if "%1"=="" (
    echo Usage: installation.bat <python_version> <config_value>
    exit /b 1
)

set python_version=%1
set config_value=%2

rem Step 1: Create a directory for organization (if it doesn't exist)
mkdir C:\HmiMonitor

rem Step 2: Download my_script.py and requirements.txt from GitHub into the folder
echo Downloading files from GitHub...
curl -o C:\HmiMonitor\HmiMonitor.py -L https://raw.githubusercontent.com/username/repository/main/my_script.py
curl -o C:\HmiMonitor\requirements.txt -L https://raw.githubusercontent.com/username/repository/main/requirements.txt

rem Step 3: Install Python dependencies using pip
echo Installing Python dependencies...
set python_exe=C:\Python%python_version%\python.exe
"%python_exe%" -m pip install -r C:\HmiMonitor\requirements.txt

rem Step 4: Install the service using NSSM
echo Installing the service using NSSM...
nssm install MyService "%python_exe%" "C:\HmiMonitor\my_script.py" --hmi_name %config_value%

echo Service installation completed.
pause