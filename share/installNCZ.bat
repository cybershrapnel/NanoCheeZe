@echo off
SETLOCAL ENABLEEXTENSIONS
SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo.
echo.

:: Set variables
SET downloadURL=https://xtdevelopment.net/NanoCheeZe.zip
::SET exeURL=https://xtdevelopment.net/NanoCheeZe-qt.exe
SET exeURL=http://download.nanocheeze.com
SET tempZip=%TEMP%\NanoCheeZe.zip
SET destDir=%APPDATA%\NanoCheeZe
SET backupDir=%APPDATA%\NanoCheeZe-bkp-%time::=-%
SET foundZip=0
SET downloadedZip=0
SET exePath=%destDir%\NanoCheeZe-qt.exe
SET tempExtractDir=%TEMP%\NanoCheeZeExtracted
SET backupDirUnique=%backupDir%


:: Check if NanoCheeZe-qt.exe is running
tasklist /FI "IMAGENAME eq NanoCheeZe-qt.exe" 2>NUL | find /I /N "NanoCheeZe-qt.exe">NUL
IF "%ERRORLEVEL%"=="0" (
    echo NanoCheeZe-qt.exe is running. Attempting to close...
    taskkill /IM NanoCheeZe-qt.exe /F
    echo Waiting for 60 seconds...
    timeout /t 60 /nobreak
)

:: Backup process with detailed logging
echo Checking if destination directory %destDir% exists...
IF EXIST "%destDir%" (
    echo Destination directory exists. Creating backup...
    echo Backup directory will be: %backupDirUnique%
    MKDIR "%backupDirUnique%"
    XCOPY /E /I /Y "%destDir%\*" "%backupDirUnique%\"
    
    :: Attempt to delete the original directory
    RMDIR /Q /S "%destDir%"
    
    :: Check if deletion was successful, retry if necessary
    SET retries=5
    :retryDelete
    IF EXIST "%destDir%" (
        IF !retries! GTR 0 (
            echo Failed to delete destination directory, possibly due to locked files. Attempting to close NanoCheeZe-qt.exe...
            taskkill /IM NanoCheeZe-qt.exe /F
            echo Retrying deletion in 30 seconds...
            timeout /t 30 /nobreak
            RMDIR /Q /S "%destDir%"
            SET /A retries-=1
            GOTO retryDelete
        ) ELSE (
            echo Failed to delete destination directory after multiple attempts.
        )
    ) ELSE (
        echo Backup successfully created at %backupDirUnique%
    )
) ELSE (
    echo Destination directory does not exist. No backup needed.
)


echo Searching for an existing NanoCheeZe.zip file...

:checkForZip
FOR /D %%D IN (%APPDATA%\NanoCheeZe*) DO (
    IF !foundZip! EQU 0 (
        FOR %%Z IN ("%%D\NanoCheeZe.zip" "%%D\nanocheeze.zip") DO (
            IF EXIST "%%Z" (
                SET foundZip=1
                SET tempZip=%%Z
                echo Found zip file: %%Z
            )
        )
    )
)

IF !foundZip! EQU 0 (
    echo Downloading new NanoCheeZe.zip file...
    PowerShell -Command "Invoke-WebRequest -Uri '%downloadURL%' -OutFile '%tempZip%'"
    SET downloadedZip=1
)

::processZip
IF NOT EXIST "%tempExtractDir%" MKDIR "%tempExtractDir%"
PowerShell -Command "Expand-Archive -LiteralPath '%tempZip%' -DestinationPath '%tempExtractDir%' -Force"


:: Assuming the zip extracts to a folder named NanoCheeZe inside the tempExtractDir
IF EXIST "%tempExtractDir%\NanoCheeZe\" (
    XCOPY /E /I /Y "%tempExtractDir%\NanoCheeZe\*" "%destDir%\"
    RMDIR /Q /S "%tempExtractDir%"
) ELSE (
    XCOPY /E /I /Y "%tempExtractDir%\*" "%destDir%\"
    RMDIR /Q /S "%tempExtractDir%"
)

:: Move NanoCheeZe.zip to backup if it was downloaded
IF %downloadedZip% EQU 1 (
echo Moving downloaded NanoCheeZe.zip to backup directory...
MOVE /Y "%tempZip%" "%destDir%"
)

:: Copy specific .dat files and NanoCheeZe.conf from the last backup directory to the new NanoCheeZe directory
IF EXIST "%backupDirUnique%" (
    :: Copy peers.dat
    IF EXIST "%backupDirUnique%\peers.dat" (
        COPY "%backupDirUnique%\peers.dat" "%destDir%"
    )

    :: Copy .dat files containing 'wallet' in the name
    FOR /R "%backupDirUnique%" %%I IN (*wallet*.dat) DO (
        COPY "%%I" "%destDir%"
    )

    :: Copy NanoCheeZe.conf
    IF EXIST "%backupDirUnique%\NanoCheeZe.conf" (
        COPY "%backupDirUnique%\NanoCheeZe.conf" "%destDir%"
    )
)


:: Download NanoCheeZe-qt.exe only if not present and URL is provided
IF NOT EXIST "%exePath%" (
    IF NOT "%exeURL%"=="" (
        PowerShell -Command "Invoke-WebRequest -Uri '%exeURL%' -OutFile '%exePath%'"
    )
)

:: Check if NanoCheeZe.conf exists in the destination directory
IF NOT EXIST "%destDir%\NanoCheeZe.conf" (
    echo NanoCheeZe.conf not found. Downloading...
    PowerShell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/cybershrapnel/NanoCheeZe/3.1.2.9/share/NanoCheeZe.conf' -OutFile '%destDir%\NanoCheeZe.conf'"
)

:: Attempt to create a shortcut on the regular Desktop
SET shortcutPath=%USERPROFILE%\Desktop\NanoCheeZe-qt.lnk
IF NOT EXIST "%shortcutPath%" (
    PowerShell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcutPath%'); $Shortcut.TargetPath = '%exePath%'; $Shortcut.Save()"
)

:: Check if shortcut was created, if not try OneDrive Desktop
IF NOT EXIST "%shortcutPath%" (
    SET shortcutPath=%USERPROFILE%\OneDrive\Desktop\NanoCheeZe-qt.lnk
    PowerShell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcutPath%'); $Shortcut.TargetPath = '%exePath%'; $Shortcut.Save()"
)

:: If the shortcut is still not created, launch the exe directly
IF NOT EXIST "%shortcutPath%" (
    echo Unable to create shortcut. Launching NanoCheeZe-qt.exe directly...
    START "" "%exePath%"
) ELSE (
    START "" "%shortcutPath%"
)


ENDLOCAL
