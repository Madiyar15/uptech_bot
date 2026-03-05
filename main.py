"""
Главный файл Telegram бота
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import BOT_TOKEN, MENU_TEXTS, BUTTON_TEXTS
from bot.keyboard.keyboards import get_main_menu_keyboard, get_courses_keyboard
from bot.handlers.menu import (
    start,
    menu_button_handler,
    handle_courses,
)
from bot.handlers.courses import (
    handle_course_selection,
    handle_course_materials,
)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def general_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Основной обработчик сообщений"""
    text = update.message.text

    # Проверка на кнопки главного меню
    if text in BUTTON_TEXTS:
        await menu_button_handler(update, context)
        return

    # Проверка на кнопку "В главное меню"
    if "В главное меню" in text or "🏠" in text:
        await update.message.reply_text(
            MENU_TEXTS["welcome"],
            reply_markup=get_main_menu_keyboard(),
        )
        context.user_data["state"] = None
        context.user_data.pop("current_course", None)
        return

    # Проверка на выбор курса
    if context.user_data.get("state") == "selecting_course":
        await handle_course_selection(update, context)
        return

    # Проверка на выбор материалов
    if context.user_data.get("state") == "selecting_materials":
        await handle_course_materials(update, context)
        return


async def post_init(app: Application) -> None:
    """Вызывается после инициализации бота"""
    logger.info("Бот успешно запущен!")


def main():
    """Стартует бота"""
    # Создание приложения
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))

    # Обработчик для всех текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, general_message_handler))

    # Запуск бота
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
