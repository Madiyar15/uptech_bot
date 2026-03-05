"""
Клавиатуры для Telegram бота
"""
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard():
    """Главное меню"""
    buttons = [
        [KeyboardButton("📚 Курсы")],
        [KeyboardButton("📖 Полезные материалы")],
        [KeyboardButton("📅 События")],
        [KeyboardButton("ℹ️ О нас")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)


def get_courses_keyboard():
    """Меню с предложением курсов"""
    buttons = [
        [KeyboardButton("Введение в нейронные сети: трансформеры и генеративные модели")],
        [KeyboardButton("Введение в нейронные сети: Python для работы с ИНС")],
        [KeyboardButton("Sage и LaTeX: применение к научным исследованиям")],
        [KeyboardButton("🏠 В главное меню")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)


def get_materials_keyboard(course_id=None):
    """Меню с материалами курса"""
    buttons = [
        [KeyboardButton("📥 Скачать материалы")],
        [KeyboardButton(" Домашние задания")],
        [KeyboardButton("⬅️ Вернуться к курсам")],
        [KeyboardButton("🏠 В главное меню")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)


def get_back_keyboard():
    """Клавиатура с кнопкой вернуться"""
    buttons = [
        [KeyboardButton("🏠 В главное меню")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
