# 🚀 Настройка CI/CD для API тестов

## Шаг 1: Добавление секретов в GitHub

1. Зайди в свой репозиторий на GitHub: https://github.com/Alextesterpro/eputs_api

2. Перейди в **Settings** → **Secrets and variables** → **Actions**

3. Нажми **New repository secret** и добавь:

   **Секрет 1:**
   - Name: `API_USERNAME`
   - Value: `a.veselov@formattwo.ru`

   **Секрет 2:**
   - Name: `API_PASSWORD`
   - Value: `твой_реальный_пароль`

✅ Теперь GitHub будет использовать эти данные для получения токена автоматически!

---

## Шаг 2: Как это работает

### Автоматические запуски:

1. **При пуше в main/develop:**
   - Каждый раз когда ты делаешь `git push`, тесты запускаются автоматически

2. **По расписанию:**
   - Каждый будний день в 12:00 МСК (9:00 UTC)
   - Можно изменить в `.github/workflows/api-tests.yml`

3. **Вручную:**
   - Заходишь в GitHub → Actions → "API Tests" → "Run workflow"

### Процесс выполнения:

```
1. Checkout кода
2. Установка Python 3.11
3. Установка зависимостей (pytest, requests, allure)
4. 🔑 Получение токена через API (логин/пароль из секретов)
5. ✅ Проверка токена
6. 🧪 Запуск тестов для всех сервисов
7. 📊 Генерация Allure отчета
8. 📢 Уведомление о результатах
```

---

## Шаг 3: Проверка работы

### После коммита файлов:

```bash
# 1. Добавь workflow файл в git
git add .github/workflows/api-tests.yml
git add CICD_SETUP.md
git commit -m "Добавили CI/CD workflow для автоматического запуска тестов"
git push origin main

# 2. Зайди на GitHub
https://github.com/Alextesterpro/eputs_api/actions

# 3. Увидишь запущенный workflow "API Tests"
```

### Запуск вручную:

1. Зайди: https://github.com/Alextesterpro/eputs_api/actions
2. Выбери "API Tests" в списке слева
3. Нажми "Run workflow" → "Run workflow"
4. Наблюдай за выполнением в реальном времени

---

## Шаг 4: Просмотр результатов

### В GitHub Actions:

- ✅ Зеленая галочка = все тесты прошли
- ❌ Красный крестик = есть падения
- 🟡 Желтый круг = тесты выполняются

### Allure отчет:

После выполнения тестов будет доступен красивый отчет с:
- Графиками прохождения тестов
- Детальной информацией об ошибках
- Историей запусков
- Трендами

---

## Дополнительные возможности

### Уведомления в Telegram/Slack:

Можно добавить отправку результатов в мессенджеры.

**Пример для Telegram:**

```yaml
- name: Отправка в Telegram
  if: always()
  run: |
    curl -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
      -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
      -d text="🧪 API Tests: ${{ job.status }}"
```

### Запуск только определенных тестов:

```bash
# В GitHub Actions можно передать параметр
pytest tests/tests_incidents/ -v -m "smoke"
```

### Запуск на разных окружениях:

```yaml
strategy:
  matrix:
    environment: [dev, staging, prod]
```

---

## Альтернатива: Использование готового токена

Если не хочешь хранить логин/пароль в секретах:

1. Получи токен локально:
   ```bash
   python3 update_token.py
   cat .env
   ```

2. Добавь токен как секрет `API_TOKEN` в GitHub

3. Измени workflow:
   ```yaml
   - name: Настройка токена
     run: |
       echo "EPUTS_TOKEN=${{ secrets.API_TOKEN }}" > .env
   ```

**Минус:** Токен протухнет через 15 дней, придется обновлять вручную.

---

## Безопасность

✅ **Что БЕЗОПАСНО:**
- Секреты в GitHub зашифрованы
- Секреты не показываются в логах
- Токены генерируются на лету

❌ **Что НЕ ДЕЛАТЬ:**
- Не коммить `.env` в git (уже в `.gitignore`)
- Не хранить пароли в коде
- Не показывать токены в логах

---

## Troubleshooting

### Ошибка: "401 Unauthorized"
- Проверь логин/пароль в секретах GitHub
- Токен мог протухнуть

### Ошибка: "Connection timeout"
- GitHub не может достучаться до API
- Возможно API недоступен извне (firewall)

### Тесты не запускаются
- Проверь синтаксис YAML файла
- Проверь что секреты добавлены
- Посмотри логи в GitHub Actions

---

## Готово! 🎉

Теперь у тебя есть полноценный CI/CD для API тестов!

