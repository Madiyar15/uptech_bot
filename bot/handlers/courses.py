"""
Обработчики для работы с курсами
"""
import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboard.keyboards import get_courses_keyboard, get_materials_keyboard, get_main_menu_keyboard
from utils.db import get_course_by_name, get_course_by_id, get_course_materials


async def handle_course_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик при выборе курса"""
    course_name = update.message.text

    # Проверка на кнопку "В главное меню"
    if "В главное меню" in course_name or "🏠" in course_name:
        context.user_data.pop("current_course", None)
        context.user_data["state"] = None
        await update.message.reply_text(
            "Что вас интересует?",
            reply_markup=get_main_menu_keyboard(),
        )
        return

    # Получаем информацию о курсе
    course = get_course_by_name(course_name)

    if course:
        text = f"""📚 {course['name']}

🌐 {course.get('name_en', 'N/A')}

👨‍🏫 Лектор: {course.get('lecturer', 'N/A')}

📝 Описание:
{course['description']}

📊 Уровень: {course.get('level', 'N/A')}
⏱️ Длительность: {course.get('duration', 'N/A')}
💰 Цена: {course.get('price', 'N/A')}

👇 Выберите действие:
"""
        context.user_data["current_course"] = course["id"]
        context.user_data["state"] = "selecting_materials"
        await update.message.reply_text(text, reply_markup=get_materials_keyboard())
    else:
        await update.message.reply_text(
            "Курс не найден. Попробуйте еще раз:",
            reply_markup=get_courses_keyboard(),
        )


async def handle_course_materials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик при скачивании материалов курса"""
    action = update.message.text
    
    # Проверка на кнопку "Вернуться к курсам"
    if "Вернуться" in action or "⬅️" in action:
        context.user_data["state"] = "selecting_course"
        context.user_data.pop("current_course", None)
        await update.message.reply_text(
            "Выберите курс:",
            reply_markup=get_courses_keyboard(),
        )
        return

    # Проверка на кнопку "В главное меню"
    if "В главное меню" in action or "🏠" in action:
        context.user_data["state"] = None
        context.user_data.pop("current_course", None)
        await update.message.reply_text(
            "Что вас интересует?",
            reply_markup=get_main_menu_keyboard(),
        )
        return

    course_id = context.user_data.get("current_course")

    if not course_id:
        await update.message.reply_text(
            "Пожалуйста, сначала выберите курс",
            reply_markup=get_courses_keyboard(),
        )
        return

    # Получить всё о курсе
    course = get_course_by_id(course_id)
    
    if not course:
        await update.message.reply_text(
            "❌ Курс не найден",
            reply_markup=get_courses_keyboard(),
        )
        return

    materials = course.get("materials", [])
    
    # Вывести все материалы, если есть
    if materials:
        await send_materials(update, context, materials, "Материалы курса")
    else:
        await update.message.reply_text(
            "❌ Материалы для этого курса недоступны",
            reply_markup=get_materials_keyboard(),
        )


async def send_materials(update: Update, context: ContextTypes.DEFAULT_TYPE, materials: list, title: str) -> None:
    """Отправляет материалы пользователю как документы"""
    if not materials:
        await update.message.reply_text(
            f"❌ Материалы недоступны",
            reply_markup=get_materials_keyboard(),
        )
        return

    # Отправляем информацию о доступных материалах
    text = f"📥 {title}:\n\n"
    for i, material in enumerate(materials, 1):
        material_type = material.get('type', 'file')
        
        # Иконка в зависимости от типа
        if material_type == 'pdf':
            icon = '📄'
        elif material_type == 'video':
            icon = '📹'
        elif material_type == 'homework':
            icon = '📝'
        elif material_type == 'code':
            icon = '💻'
        elif material_type == 'document':
            icon = '📑'
        else:
            icon = '📎'
        
        text += f"{i}. {icon} {material['name']}\n"

    await update.message.reply_text(text)

    # Отправляем каждый файл как документ
    for material in materials:
        file_path = material.get('file_path') or material.get('url')
        
        # Проверяем, это локальный файл (путь) или URL
        if file_path and os.path.exists(file_path):
            try:
                # Отправляем как документ
                with open(file_path, 'rb') as f:
                    document_name = material.get('name', os.path.basename(file_path))
                    await update.message.reply_document(
                        document=f,
                        caption=f"📎 {document_name}",
                        filename=os.path.basename(file_path)
                    )
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Ошибка при отправке файла: {material['name']}\n{str(e)}"
                )
        elif file_path and file_path.startswith('http'):
            # Если это URL, отправляем как ссылку
            icon = '🔗'
            await update.message.reply_text(
                f"{icon} {material['name']}\n{file_path}"
            )
        else:
            await update.message.reply_text(
                f"❌ Файл не найден: {material['name']}"
            )

    # Показываем клавиатуру после отправки всех файлов
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=get_materials_keyboard()
    )
