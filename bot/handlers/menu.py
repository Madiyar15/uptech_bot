"""
Обработчики основного меню
"""
import os
from telegram import Update
from telegram.ext import ContextTypes
from config import MENU_TEXTS, BASE_DIR
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
    # Выводим информацию о ресурсах
    text = """📖 Полезные материалы

🔗 Математические основы МО и ИНС - QuData
https://qudata.com/ml/ru/
📝 Полный курс с математическими основами машинного обучения и искусственных нейронных сетей

🔗 Math Hedgehog - YouTube канал
https://www.youtube.com/@math_hedgehog
📺 Видео-уроки по математике и машинному обучению
"""
    await update.message.reply_text(text)

    # Файлы материалов
    materials_files = [
        ("codelibs.ru_mashinnoe-obuchenie-osnovy.pdf", "Машинное обучение основы (CodeLibs.ru)"),
        ("Nikolenko_S_I_Kadurin_A_A_Arkhangelskaya_E_O_Glubokoe_obuchenie.pdf", "Глубокое обучение (Николенко, Кадурин, Архангельская)"),
        ("data/materials/Latex_My_Tutorial-5 (2) (2).pdf", "LaTeX Туториал"),
        ("data/materials/Файл_про_Научные_работы.pdf", "Файл про Научные работы"),
    ]

    # Отправляем каждый файл
    for file_path, display_name in materials_files:
        # Преобразуем относительный путь в абсолютный
        if not os.path.isabs(file_path):
            full_path = os.path.join(BASE_DIR, file_path)
        else:
            full_path = file_path

        # Проверяем, существует ли файл
        if os.path.exists(full_path):
            try:
                with open(full_path, 'rb') as f:
                    await update.message.reply_document(
                        document=f,
                        caption=f"📎 {display_name}",
                        filename=os.path.basename(full_path)
                    )
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Ошибка при отправке файла {display_name}: {str(e)}"
                )

    # Показываем кнопку возврата
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=get_back_keyboard()
    )


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
