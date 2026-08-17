@echo off
setlocal enabledelayedexpansion

:ask
set /p drive="Enter drive letter (e.g., E): "

:: Remove colon if user included it
set drive=%drive::=%

:: Check if drive is A, B, C, or D (case insensitive)
if /i "%drive%"=="A" goto invalid
if /i "%drive%"=="B" goto invalid
if /i "%drive%"=="C" goto invalid
if /i "%drive%"=="D" goto invalid

:: Check if drive exists
if not exist %drive%:\ goto invalid

:: Check if FFmpeg is installed
where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo FFmpeg not found! Please install FFmpeg and add it to your PATH.
    pause
    exit /b 1
)

cd /d %drive%:\DCIM 2>nul
if errorlevel 1 (
    echo DCIM folder not found on drive %drive%:
    goto ask
)

echo Processing files...
for /d %%i in (*_PANA) do (
    echo Entering folder: %%i
    pushd "%%i"
    for %%f in (*.mov) do (
        echo Converting: %%f
        
        :: Check if JPG with same name exists and delete it
        if exist "%%~nf.jpg" (
            echo Deleting existing JPG: %%~nf.jpg
            del "%%~nf.jpg"
        )
        
        :: Convert MOV to GIF
        ffmpeg -i "%%f" -vf "fps=10" -c:v gif -f gif "%%~nf.gif"
        if errorlevel 1 (
            echo Failed to convert %%f
        ) else (
            echo Successfully created %%~nf.gif
            :: Delete the original MOV file after successful conversion
            echo Deleting original MOV: %%f
            del "%%f"
        )
    )
    popd
)

echo Done!
pause
exit /b 0

:invalid
echo Drive %drive%: is not allowed or does not exist.
echo Please use drives E through Z.
goto ask