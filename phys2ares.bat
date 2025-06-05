@echo off
setlocal enabledelayedexpansion

REM Check for two arguments
if "%~2"=="" (
    echo Usage: %~nx0 ^<Save File^> ^<ROM file^>
    exit /b 1
)

set "save_file=%~1"
set "rom=%~2"

REM Extract the extension
for %%F in ("%save_file%") do set "ext=%%~xF"
set "ext=!ext:~1!"

REM Determine new extension
if /i "%ext%"=="fla" (
    set "new_ext=flash"
) else if /i "%ext%"=="sra" (
    set "new_ext=ram"
) else if /i "%ext%"=="eep" (
    set "new_ext=eeprom"
) else (
    echo Invalid Save File Type
    echo Usage: %~nx0 ^<Save File^> ^<ROM file^>
    exit /b 1
)

REM Build new filename and rename
set "new_file=%rom%.%new_ext%"

ren "%save_file%" "%~nx2.%new_ext%"
echo Renamed "%save_file%" to "%new_file%"

