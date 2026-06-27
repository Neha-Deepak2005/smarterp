@echo off
echo Starting SmartERP...
net start mysql80
cd C:\Users\DEEPS\smarterp
python app.py
pause