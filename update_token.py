#!/usr/bin/env python3
"""
Скрипт для обновления токена в .env файле
Использует логин и пароль для получения нового токена
"""

import requests
import os
import sys


def login_and_get_token(username, password):
    """
    Выполнить логин и получить токен
    """
    url = "http://91.227.17.139/services/passport/api/login"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://91.227.17.139",
        "Pragma": "no-cache",
        "Referer": "http://91.227.17.139/signin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "service": "eputs"
    }
    
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        print(f"Отправка запроса на логин для пользователя: {username}")
        response = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Попытка найти токен в разных полях ответа
            token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")
            
            if token:
                print(f"Токен успешно получен (длина: {len(token)} символов)")
                return token
            else:
                print(f"Токен не найден в ответе. Ответ: {data}")
                return None
        else:
            print(f"Ошибка логина: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"Ошибка при логине: {e}")
        return None


def save_token_to_env(token):
    """
    Сохранить токен в .env файл
    """
    env_file = ".env"
    
    # Читаем существующий .env
    lines = []
    token_found = False
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
    
    # Обновляем или добавляем токен
    with open(env_file, 'w') as f:
        for line in lines:
            if line.startswith('EPUTS_TOKEN='):
                f.write(f'EPUTS_TOKEN={token}\n')
                token_found = True
            else:
                f.write(line)
        
        # Если токена не было в файле, добавляем его
        if not token_found:
            f.write(f'EPUTS_TOKEN={token}\n')
    
    print(f"Токен сохранен в {env_file}")


def check_token_validity():
    """
    Проверить валидность сохраненного токена
    """
    try:
        from api_client_incidents import SimpleAPIClient
        
        client = SimpleAPIClient()
        result = client.check_token()
        
        print("\nПроверка токена:")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        return result['valid']
        
    except Exception as e:
        print(f"Ошибка при проверке токена: {e}")
        return False


def main():
    """
    Основная функция
    """
    print("=" * 60)
    print("ОБНОВЛЕНИЕ ТОКЕНА ДЛЯ API")
    print("=" * 60)
    
    # Получаем креды из переменных окружения или запрашиваем у пользователя
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
    if not username:
        username = input("Введите username: ").strip()
    else:
        print(f"Используется username из переменной окружения: {username}")
    
    if not password:
        import getpass
        password = getpass.getpass("Введите password: ").strip()
    else:
        print("Используется password из переменной окружения")
    
    if not username or not password:
        print("Ошибка: username и password обязательны!")
        sys.exit(1)
    
    # Получаем токен
    token = login_and_get_token(username, password)
    
    if not token:
        print("\nОшибка: не удалось получить токен!")
        sys.exit(1)
    
    # Сохраняем токен
    save_token_to_env(token)
    
    # Проверяем токен
    if check_token_validity():
        print("\n" + "=" * 60)
        print("УСПЕХ: Токен обновлен и работает!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ВНИМАНИЕ: Токен обновлен, но проверка не прошла!")
        print("=" * 60)


if __name__ == "__main__":
    # Отключаем предупреждения SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()

