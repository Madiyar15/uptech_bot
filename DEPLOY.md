# 🚀 Инструкция по развертыванию бота на Railway

## Шаг 1: Подготовка кода

Все файлы уже готовы для деплоя! ✅

## Шаг 2: Создание GitHub репозитория

1. Если у вас нет Instagram аккаунта - создайте на https://github.com/signup
2. Создайте новый репозиторий:
   - Нажимите `+` → `New repository`
   - Название: `uptech-bot`
   - Сделайте его **Public** (важно для деплоя)
   - Нажмите `Create repository`

3. На вашем компьютере откройте PowerShell в папке проекта:
```powershell
cd C:\Users\admin\OneDrive\Desktop\uptech_bot
```

4. Инициализируйте Git репозиторий:
```powershell
git init
git add .
git commit -m "Initial commit: UpTech Bot"
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/uptech-bot.git
git push -u origin main
```

## Шаг 3: Развертывание на Railway

1. Откройте https://railway.app
2. Нажмите `Login` → `Login with GitHub`
3. Разрешите доступ к вашим репозиториям
4. На главной странице нажмите `+ New Project` → `Deploy from GitHub repo`
5. Выберите репозиторий `uptech-bot`
6. Railway автоматически обнаружит и запустит бота

## Шаг 4: Добавление BOT_TOKEN

1. На странице проекта нажмите на сервис (рабочий процесс)
2. Перейдите на вкладку `Variables`
3. Добавьте переменную:
   - **Key**: `BOT_TOKEN`
   - **Value**: Ваш токен от @BotFather
4. Нажмите `Add` и затем `Deploy`

## Шаг 5: Обновление config.py для использования переменных окружения

Немного модифицируем конфиг, чтобы читал переменную окружения:

```python
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# остальной код...
```

## Результат

✅ Бот будет работать 24/7!
✅ Автоматический перезапуск при падении
✅ Логи доступны в Railway
✅ Легко обновить код - просто push на GitHub

---

## Альтернативные варианты

### Render.com (если Railway не подходит)

1. Откройте https://render.com
2. Нажмите `Dashboard` → `New Service`
3. Выберите `Web Service` → GitHub
4. Выберите ваш репозиторий
5. Настройки:
   - **Name**: uptech-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. Добавьте BOT_TOKEN в `Environment Variables`
7. Deploy!

⚠️ Минус: засыпает через 15 минут неактивности (нужен uptimer)

### Replit.com (самый простой вариант)

1. Откройте https://replit.com
2. Нажмите `Create Repl` → `Import from GitHub`
3. Вставьте URL вашего репозитория
4. Добавьте переменные в `.replit`:
```
run = "python main.py"
```
5. Нажмите `Run`

---

## Возможные проблемы и решения

### Проблема: "ModuleNotFoundError: No module named 'telegram'"

**Решение**: 
```bash
pip install -r requirements.txt
```

### Проблема: BOT_TOKEN не работает

**Решение**: Убедитесь, что переменная окружения установлена на сервере

### Проблема: Бот работает но не отвечает

**Решение**: 
- Проверьте, что BOT_TOKEN правильный
- Проверьте логи на Railway/Render
- Убедитесь, что интернет соединение активно

---

**Рекомендую Railway - это самый надежный вариант для Telegram ботов!** 🚀
