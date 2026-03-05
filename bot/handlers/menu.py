"""
Обработчики основного меню
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import MENU_TEXTS
from bot.keyboard.keyboards import (
    get_main_menu_keyboard,
    get_courses_keyboard,
    get_back_keyboard,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n{MENU_TEXTS['welcome']}",
        reply_markup=get_main_menu_keyboard(),
    )


async def menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопок главного меню"""
    text = update.message.text

    if text == "📚 Курсы":
        await handle_courses(update, context)
    elif text == "📖 Полезные материалы":
        await handle_useful_materials(update, context)
    elif text == "📅 События":
        await handle_events(update, context)
    elif text == "ℹ️ О нас":
        await handle_about(update, context)


async def handle_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопки Курсы"""
    context.user_data["state"] = "selecting_course"
    await update.message.reply_text(
        MENU_TEXTS["courses"],
        reply_markup=get_courses_keyboard(),
    )


async def handle_useful_materials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопки Полезные материалы"""
    text = """📖 Полезные материалы

1. 📚 Официальная документация Python
   https://docs.python.org

2. 📘 Real Python Tutorials
   https://realpython.com

3. 🎥 YouTube каналы для программистов
   - Programming with Mosh
   - Traversy Media
   - Corey Schafer

4. 📱 Мобильные приложения для обучения
   - Codecademy
   - SoloLearn
   - HackerRank
"""
    await update.message.reply_text(text, reply_markup=get_back_keyboard())


async def handle_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопки События"""
    text = """📅 События и вебинары

📌 Предстоящие события:

Официальное открытие UpTech 🚀

10 марта в 14:10 в аудитории 111 :
— расскажем о проекте и команде 👥
— обсудим программу обучения 📖
— покажем сайт и Telegram-бота 💻
— поделимся планами развития и перспективами 📈
— познакомимся с вами и соберём ваши идеи💡
— а ещё будет специальный гость 🤫

Ждём каждого, кто хочет расти в IT и быть частью комьюнити 🔥 

Адрес: Казахстанский филиал МГУ, улица Кажымукана 11
"""
    await update.message.reply_text(text, reply_markup=get_back_keyboard())


async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопки О нас"""
    text = """ℹ️ О нас

Всем привет! Если хочешь развиваться в IT, то мы приглашаем тебя в UpTech — это IT-сообщество, где ты сможешь начать и развивать свой путь.

В UpTech ты получишь:
• участие в проектах и практический опыт;
• встречи с представителями из IT-сферы;
• менторство и тренировочные собеседования;
• окружение студентов с такими же целями;
• понимание, как ворваться в IT и построить свою карьеру.

Мы помогаем пройти путь от новичка до уверенного специалиста.

Если интересно - переходи по ссылке и жди ближайшие новости о предстоящих событиях.

📞 Свяжитесь с нами:
📧 Email: uptech.community@gmail.com
"""
    await update.message.reply_text(text, reply_markup=get_back_keyboard())
