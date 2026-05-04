#!/bin/bash
# Скрипт запуска для Linux и macOS

# Проверка наличия venv
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация и установка зависимостей
source venv/bin/activate
echo "Проверка зависимостей..."
pip install -r requirements.txt --quiet

# Запуск программы
python3 main.py
