# Управление токеном авторизации

## Как работает токен

Токен хранится в файле `.env` в корне проекта:

```
EPUTS_TOKEN=ваш_токен_здесь
```

## Проверка токена

### Способ 1: Через pytest тесты

```bash
# Проверить токен для всех API
python3 -m pytest tests/test_api_info.py::TestTokenCheck -v -s

# Только для API инцидентов
python3 -m pytest tests/test_api_info.py::TestTokenCheck::test_incidents_token_check -v -s

# Только для API ДТП
python3 -m pytest tests/test_api_info.py::TestTokenCheck::test_dtp_token_check -v -s
```

### Способ 2: Через Python скрипт

```python
from api_client_incidents import SimpleAPIClient

client = SimpleAPIClient()
result = client.check_token()

print(f"Валиден: {result['valid']}")
print(f"Статус: {result['status_code']}")
print(f"Сообщение: {result['message']}")
```

## Обновление токена

### Вариант 1: Автоматически через скрипт (рекомендуется)

```bash
python3 update_token.py
```

Скрипт запросит:
- username
- password

Затем автоматически:
1. Выполнит логин
2. Получит новый токен
3. Сохранит его в `.env`
4. Проверит валидность

### Вариант 2: Через переменные окружения

```bash
export API_USERNAME="a.veselov@formattwo.ru"
export API_PASSWORD="ваш_пароль"
python3 update_token.py
```

### Вариант 3: Вручную

1. Выполните логин через curl:

```bash
curl 'http://91.227.17.139/services/passport/api/login' \
  -H 'Content-Type: application/json' \
  -H 'service: eputs' \
  --data-raw '{"username":"ваш_логин","password":"ваш_пароль"}' \
  --insecure
```

2. Скопируйте токен из ответа (поле `token` или `access_token`)

3. Обновите файл `.env`:

```
EPUTS_TOKEN=новый_токен
```

## Что делать если токен протух

Признаки протухшего токена:
- Тесты падают с ошибкой 401 (Unauthorized)
- API возвращает ошибку авторизации
- `check_token()` возвращает `valid: False`

**Решение:**

```bash
python3 update_token.py
```

## Возможные ошибки

### 401 Unauthorized
**Причина:** Токен протух или невалиден  
**Решение:** Обновите токен через `update_token.py`

### 403 Forbidden
**Причина:** Нет доступа к ресурсу  
**Решение:** Проверьте права пользователя

### Токен не найден
**Причина:** Файл `.env` отсутствует или пустой  
**Решение:** Создайте `.env` файл и обновите токен

## Структура проверки токена

```python
result = {
    "valid": True/False,           # Валиден ли токен
    "status_code": 200,            # HTTP статус код
    "message": "Токен валиден"     # Сообщение о результате
}
```

### Возможные статусы:

- `200` - Токен валиден
- `401` - Токен протух или невалиден
- `403` - Нет доступа
- `0` - Ошибка соединения

## Автоматизация

Для автоматического обновления токена в CI/CD добавьте переменные окружения:

```yaml
env:
  API_USERNAME: ${{ secrets.API_USERNAME }}
  API_PASSWORD: ${{ secrets.API_PASSWORD }}

script:
  - python3 update_token.py
  - pytest tests/
```

## Безопасность

- **НЕ КОММИТЬТЕ** файл `.env` в git!
- `.env` добавлен в `.gitignore`
- Используйте переменные окружения для CI/CD
- Регулярно обновляйте пароль

## FAQ

**Q: Как часто нужно обновлять токен?**  
A: Токены обычно действуют 24-48 часов. Рекомендуется обновлять перед каждым запуском тестов или при ошибке 401.

**Q: Можно ли автоматически обновлять токен в тестах?**  
A: Да, можно добавить фикстуру в `conftest.py` которая будет проверять токен перед запуском тестов и обновлять при необходимости.

**Q: Какой токен используется - incidents или dtp?**  
A: Один и тот же токен используется для обоих API, только с разными заголовками `service: eputs` и `service: dtp`.

**Q: Что делать если `update_token.py` не работает?**  
A: Проверьте креды, доступность API, или обновите токен вручную через curl.

