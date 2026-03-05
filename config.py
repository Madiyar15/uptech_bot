"""
Конфигурация Telegram бота
"""
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Путь к корневой папке проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Получить токен из переменной окружения или использовать значение по умолчанию
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Основная информация
BOT_NAME = "UpTech Bot"

# Тексты для меню
MENU_TEXTS = {
    "welcome": "Добро пожаловать в UpTech Bot! 🎓\nЧто вас интересует?",
    "courses": "Выберите курс:",
    "materials": "Материалы курса:",
    "useful_materials": "Полезные материалы",
    "events": "События и вебинары",
    "about": "О нас",
}

# Кнопки главного меню
MAIN_MENU_BUTTONS = ["📚 Курсы", "📖 Полезные материалы", "📅 События", "ℹ️ О нас"]

# Текст для каждой кнопки
BUTTON_TEXTS = {
    "📚 Курсы": "courses",
    "📖 Полезные материалы": "useful_materials",
    "📅 События": "events",
    "ℹ️ О нас": "about",
}
