@echo off

REM ________________________________________________________________

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (

    echo asking for administrator's guide

    goto UACPrompt

) else ( goto gotAdmin )

:UACPrompt

    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"

    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"

    exit /B

:gotAdmin

    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )

    pushd "%CD%"

    CD /D "%~dp0"

REM ________________________________________________________________

REG ADD HKEY_CLASSES_ROOT\*\shell\PaperNamer\command /ve /t REG_SZ /d "%~dp0papernamer.cmd \"%%1\"" /f
REG ADD HKEY_CLASSES_ROOT\*\shell\PaperNamer /v Icon /t REG_SZ /d "%~dp0\pdf.ico" /f