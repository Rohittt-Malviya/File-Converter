@echo off
call .venv\Scripts\activate
pyinstaller --noconfirm --clean --name LocalConvert --windowed --paths . desktop\frontend\main.py
if not exist deploy\desktop\windows mkdir deploy\desktop\windows
xcopy /E /I /Y dist\LocalConvert* deploy\desktop\windows
