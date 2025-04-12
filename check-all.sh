#!/bin/bash

echo "🔍 Проверка каждого локального порта через curl:"
for PORT in $(seq 5000 5019); do
    echo -e "\n🧪 Порт $PORT"
    curl --max-time 10 --proxy socks5h://client:clientpass@127.0.0.1:$PORT http://ip-api.com/json
done
