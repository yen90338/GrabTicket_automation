@echo off
cd /d "C:\Users\F018\Desktop\GrabTicket_automation"

:: 將所有修改加入暫存區
git add .

:: 提示輸入 commit 訊息
set /p msg=輸入 commit 訊息：

:: 執行 commit 和 push
git commit -m "%msg%"
git push origin main

pause
