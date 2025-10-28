#!/usr/bin/env python3
"""
Автоматическое обновление токена
Использует credentials из переменных окружения или из .env файла
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


def get_new_token():
    """Получить новый токен через API"""
    # Пробуем получить credentials из переменных окружения
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
    if not username or not password:
        print("Ошибка: API_USERNAME или API_PASSWORD не найдены в .env файле!")
        print("\nДобавьте в .env файл:")
        print("API_USERNAME=your_username")
        print("API_PASSWORD=your_password")
        return None
    
    url = "http://91.227.17.139/services/passport/api/login"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "service": "eputs"
    }
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        print(f"Получение токена для пользователя: {username}")
        response = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")
            
            if token:
                print(f"Токен успешно получен (длина: {len(token)} символов)")
                return token
            else:
                print(f"Токен не найден в ответе")
                print(f"Ответ: {data}")
                return None
        else:
            print(f"Ошибка авторизации: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"Ошибка при получении токена: {e}")
        return None


def save_token(token):
    """Сохранить токен в .env файл"""
    # Читаем существующий .env
    env_lines = []
    env_path = ".env"
    
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            env_lines = f.readlines()
    
    # Обновляем или добавляем токены
    token_vars = {
        "EPUTS_TOKEN": token,
        "API_TOKEN": token
    }
    
    updated_vars = set()
    new_env_lines = []
    
    for line in env_lines:
        updated = False
        for var_name in token_vars:
            if line.startswith(f"{var_name}="):
                new_env_lines.append(f"{var_name}={token}\n")
                updated_vars.add(var_name)
                updated = True
                break
        if not updated:
            new_env_lines.append(line)
    
    # Добавляем новые переменные если их не было
    for var_name, var_value in token_vars.items():
        if var_name not in updated_vars:
            new_env_lines.append(f"{var_name}={var_value}\n")
    
    # Сохраняем обратно
    with open(env_path, "w") as f:
        f.writelines(new_env_lines)
    
    print(f"Токен сохранен в {env_path}")


def main():
    print("=" * 60)
    print("АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ ТОКЕНА")
    print("=" * 60)
    
    # Получаем новый токен
    token = get_new_token()
    
    if not token:
        print("\nОшибка: не удалось получить токен!")
        sys.exit(1)
    
    # Сохраняем токен
    save_token(token)
    
    print("\n" + "=" * 60)
    print("УСПЕХ: Токен обновлен!")
    print("=" * 60)
    print("\nТеперь можно запустить тесты:")
    print("  pytest tests/tests_water_transport/ -v")


if __name__ == "__main__":
    # Отключаем предупреждения о незащищенных HTTPS запросах
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()

