#!/bin/bash

# Проверяем наличие .env файла
if [ ! -f .env ]; then
  echo "Файл .env не найден. Создаем шаблон..."
  echo "YC_FOLDER_ID=your_folder_id_here" > .env
  echo "YC_API_KEY=your_api_key_here" >> .env
  echo "Пожалуйста, заполните файл .env корректными данными и перезапустите скрипт."
  exit 1
fi

# Проверяем, заполнены ли переменные в .env
source .env
if [ -z "$YC_FOLDER_ID" ] || [ "$YC_FOLDER_ID" == "your_folder_id_here" ]; then
  echo "Пожалуйста, укажите корректный YC_FOLDER_ID в файле .env"
  exit 1
fi

if [ -z "$YC_API_KEY" ] && [ -z "$YC_IAM_TOKEN" ]; then
  echo "Пожалуйста, укажите YC_API_KEY или YC_IAM_TOKEN в файле .env"
  exit 1
fi

# Устанавливаем зависимости
echo "Устанавливаем зависимости..."
pip install -r requirements.txt

# Применяем настройки Cline
echo "Применяем настройки Cline для VS Code..."
mkdir -p ~/.vscode/extensions/cline-custom-provider
cp cline_settings.json ~/.vscode/extensions/cline-custom-provider/

# Запускаем сервер
echo "Запускаем сервер YandexCloud ML для Cline..."
python cline_server.py
