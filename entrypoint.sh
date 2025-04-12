#!/bin/bash

echo "[*] Генерация конфигурации..."
python3 /generate_gost_config.py

echo "[*] Запуск gost..."
exec gost -C gost.yaml
