@echo off
REM Скрипт запуска для Windows

if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)

call venv\Scripts\activate
echo Проверка зависимостей...
pip install -r requirements.txt --quiet

python main.py
pause
