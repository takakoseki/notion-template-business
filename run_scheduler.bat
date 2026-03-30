@echo off
cd /d "C:\Users\tkoseki\notion-template-business"
if not exist logs mkdir logs
venv\Scripts\python.exe scheduler.py >> logs\scheduler.log 2>&1
