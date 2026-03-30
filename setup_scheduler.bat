@echo off
setlocal

set TASK_NAME=NotionTemplateScheduler
set ROOT=C:\Users\tkoseki\notion-template-business
set VBS=%ROOT%\run_scheduler.vbs
set LOG=%ROOT%\logs\scheduler.log

echo ============================================================
echo  Notion Template Scheduler - Windows Task Scheduler Setup
echo ============================================================
echo.
echo Task name : %TASK_NAME%
echo Runner    : %VBS%
echo Log       : %LOG%
echo Trigger   : On logon (current user)
echo.

schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%VBS%\"" /sc ONLOGON /f

if %ERRORLEVEL% equ 0 (
    echo.
    echo [OK] Task registered successfully.
    echo      scheduler.py will start automatically at next login.
    echo      Running in the background with no window.
    echo      Log output: %LOG%
    echo.
    echo ---- Other commands ----------------------------------------
    echo  Run now    : schtasks /run /tn "%TASK_NAME%"
    echo  Check status: schtasks /query /tn "%TASK_NAME%"
    echo  Remove task : schtasks /delete /tn "%TASK_NAME%" /f
    echo ------------------------------------------------------------
) else (
    echo.
    echo [ERROR] Failed to register task.
    echo         Right-click setup_scheduler.bat and select "Run as administrator".
)

echo.
pause
endlocal
