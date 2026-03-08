"""
Обработчики для поиска видео на YouTube
"""
import yt_dlp
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboard.keyboards import get_main_menu_keyboard


async def handle_video_search_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик запроса на поиск видео"""
    context.user_data["state"] = "searching_video"
    await update.message.reply_text(
        "🔍 Введите название видео для поиска на YouTube:",
    )


async def search_youtube_videos(query: str, max_results: int = 10) -> list:
    """Поиск видео на YouTube через yt-dlp"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Поиск видео
            search_query = f"ytsearch{max_results}:{query}"
            results = ydl.extract_info(search_query, download=False)

            videos = []
            if results and 'entries' in results:
                for entry in results['entries']:
                    video_info = {
                        'title': entry.get('title', 'Неизвестное название'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                        'duration': entry.get('duration', 0),
                        'channel': entry.get('channel', 'Неизвестный канал'),
                    }
                    videos.append(video_info)

            return videos
    except Exception as e:
        print(f"Ошибка при поиске видео: {str(e)}")
        return []


async def handle_video_search_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик результатов поиска видео"""
    search_query = update.message.text

    if not search_query or len(search_query) < 2:
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректный поисковый запрос (минимум 2 символа)"
        )
        return

    # Показываем статус поиска
    status_message = await update.message.reply_text(
        f"🔍 Ищу видео: '{search_query}'...\n⏳ Это может занять несколько секунд"
    )

    # Ищем видео
    videos = await search_youtube_videos(search_query, max_results=10)

    # Удаляем сообщение о поиске
    try:
        await status_message.delete()
    except:
        pass

    if not videos:
        await update.message.reply_text(
            f"❌ Видео по запросу '{search_query}' не найдены.\n\nПопробуйте другой поисковый запрос.",
            reply_markup=get_main_menu_keyboard(),
        )
        context.user_data["state"] = None
        return

    # Форматируем результаты
    text = f"🎥 Результаты поиска для: '{search_query}'\n\n"
    text += "Найдено видео:\n\n"

    for i, video in enumerate(videos, 1):
        # Форматируем длительность
        duration = video.get('duration', 0)
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"
        else:
            duration_str = "?"

        text += f"{i}. 🎬 {video['title']}\n"
        text += f"   📺 {video['channel']}\n"
        text += f"   ⏱️ {duration_str} мин\n"
        text += f"   🔗 {video['url']}\n\n"

    await update.message.reply_text(
        text,
        reply_markup=get_main_menu_keyboard(),
        disable_web_page_preview=True,
    )

    context.user_data["state"] = None
