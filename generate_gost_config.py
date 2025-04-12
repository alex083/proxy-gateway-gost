import requests
import yaml
import socket
import os

API_URL = os.getenv("API_URL", "https://api.runonflux.io/apps/location/proxypoolusa")
REMOTE_PORT = int(os.getenv("REMOTE_PORT", 3408))
REMOTE_USER = os.getenv("REMOTE_USER", "user")
REMOTE_PASS = os.getenv("REMOTE_PASS", "pass")
CLIENT_USER = os.getenv("CLIENT_USER", "client")
CLIENT_PASS = os.getenv("CLIENT_PASS", "clientpass")
START_PORT = int(os.getenv("START_PORT", 5000))
MAX_PROXIES = int(os.getenv("MAX_PROXIES", 55))

def is_proxy_alive(ip, port=REMOTE_PORT, timeout=3):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def generate_config():
    print("[*] Получаем список IP с API...")
    response = requests.get(API_URL)
    data = response.json()

    ip_list = list({item['ip'].split(':')[0] for item in data['data']})
    print(f"[+] Уникальных IP: {len(ip_list)}")

    config = {
        "services": [],
        "auth": [
            {
                "username": CLIENT_USER,
                "password": CLIENT_PASS
            }
        ]
    }

    port = START_PORT
    added = 0

    for ip in ip_list:
        if added >= MAX_PROXIES:
            break

        print(f"[~] Проверка {ip}:{REMOTE_PORT}...", end=' ')
        if is_proxy_alive(ip, REMOTE_PORT):
            print("✅")
            service = {
                "name": f"proxy-{port}",
                "addr": f":{port}",
                "handler": {
                    "type": "socks5",
                    "auth": {
                        "username": CLIENT_USER,
                        "password": CLIENT_PASS
                    }
                },
                "forwarder": {
                "reuse": False,
                    "nodes": [
                        {
                            "addr": f"{ip}:{REMOTE_PORT}",
                            "username": REMOTE_USER,
                            "password": REMOTE_PASS
                        }
                    ]
                }
            }
            config["services"].append(service)
            port += 1
            added += 1
        else:
            print("❌")

    with open("gost.yaml", "w") as f:
        yaml.dump(config, f)

    print(f"[✓] Конфигурация создана: {added} прокси записано в gost.yaml")

if __name__ == "__main__":
    generate_config()
