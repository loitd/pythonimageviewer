@echo off
rem pip install PyInstaller tinyaes
rem SYNTAX: lbuild.bat main.py main
rem pyinstaller also works on Linux, MacOS, FreeBSD, OpenBSD, ... https://pyinstaller.readthedocs.io/en/stable/requirements.html#gnu-linux
rem pyinstaller creates X86 or x64 architecture based on current Python architecture
setlocal
CALL :GETPARENT PARENT
echo "Checking environment"
IF /I "%PARENT%" == "powershell" GOTO :ISPOWERSHELL
IF /I "%PARENT%" == "pwsh" GOTO :ISPOWERSHELL
endlocal

echo "You are Command Prompt"
set fullname=%1
set filename=%fullname:~0,-2%
set output=%2
echo [Command] Building standalone onefile ... %1
rem -D: onedir -F: onefile -n: Name -y: No confirm, -p: add path --key: key to encrypt. UPX breaking vcruntime140.dll (64bit) => VCRUNTIME140.dll MUST === 84kb
rem -p C:\\Windows\\System32\\downlevel ^
pyinstaller --clean -D -y -w ^
    -p venv\\Lib\\site-packages ^
    --key=lL02Hkiuh192lllp ^
    --upx-dir=D:\\setup\\upx-3.96-win64 ^
    --upx-exclude=vcruntime140.dll ^
    --add-data piv.ico;. ^
    --add-data piv.png;. ^
    --add-data open.gif;. ^
    --add-data exit.gif;. ^
    --version-file=version.rc ^
    -i piv.ico -n %2 %1
echo [Command] Build finished. Your module built in build. Your program (standalone) in dist folder.
GOTO :EOF

:GETPARENT
SET "PSCMD=$ppid=$pid;while($i++ -lt 3 -and ($ppid=(Get-CimInstance Win32_Process -Filter ('ProcessID='+$ppid)).ParentProcessId)) {}; (Get-Process -EA Ignore -ID $ppid).Name"
for /f "tokens=*" %%i in ('powershell -noprofile -command "%PSCMD%"') do SET %1=%%i
GOTO :EOF

:ISPOWERSHELL
echo "You are PowerShell. Not support PowerShell yet."
