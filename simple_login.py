#!/usr/bin/env python3
"""
Простой скрипт для авторизации
"""

import requests
import json


def login():
    """Авторизация и получение токена"""
    print("🔐 Авторизация...")
    
    # Данные для входа
    url = "http://91.227.17.139/services/passport/api/login"
    data = {
        "username": "a.veselov@formattwo.ru",
        "password": "#020C66c60af"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "service": "eputs"
    }
    
    # Отправляем запрос
    response = requests.post(url, json=data, headers=headers, verify=False)
    
    print(f"Статус: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        token = result.get('access_token')
        
        if token:
            # Сохраняем токен в файл
            with open('.env', 'w') as f:
                f.write(f"EPUTS_TOKEN={token}\n")
            
            print(f"✅ Токен получен: {token[:20]}...")
            print("💾 Токен сохранен в .env файл")
            return True
        else:
            print("❌ Токен не найден в ответе")
            return False
    else:
        print(f"❌ Ошибка авторизации: {response.text}")
        return False


if __name__ == "__main__":
    if login():
        print("\n🎉 Авторизация успешна!")
        print("Теперь можно запустить: python3 simple_tests.py")
    else:
        print("\n❌ Авторизация не удалась")
