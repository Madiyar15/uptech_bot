"""
Обработчики для поиска видео на YouTube
"""
import yt_dlp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboard.keyboards import get_main_menu_keyboard
import urllib.parse

# Пул потоков для yt-dlp
executor = ThreadPoolExecutor(max_workers=1)


def search_youtube_sync(query: str, max_results: int = 10) -> list:
    """Синхронный поиск видео на YouTube (работает в отдельном потоке)"""
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'socket_timeout': 30,
        'default_search': 'ytsearch',
    }

    videos = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"[DEBUG] Ищу на YouTube: {query}")
            
            # Формируем поисковый запрос
            search_query = f"ytsearch{max_results}:{query}"
            print(f"[DEBUG] Запрос: {search_query}")
            
            # Выполняем поиск
            results = ydl.extract_info(search_query, download=False)
            print(f"[DEBUG] Получены результаты: {type(results)}")

            if results and 'entries' in results:
                print(f"[DEBUG] Найдено entries: {len(results['entries'])}")
                
                for idx, entry in enumerate(results['entries']):
                    if not entry:
                        continue
                        
                    try:
                        video_id = entry.get('id')
                        title = entry.get('title', 'Неизвестное название')
                        duration = entry.get('duration', 0)
                        channel = entry.get('channel', 'Неизвестный канал')
                        
                        if not video_id:
                            print(f"[DEBUG] Пропуск видео {idx} - нет video_id")
                            continue
                        
                        video_info = {
                            'title': title,
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'duration': duration,
                            'channel': channel,
                        }
                        videos.append(video_info)
                        print(f"[DEBUG] Добавлено видео: {title}")
                    except Exception as e:
                        print(f"[DEBUG] Ошибка при обработке видео {idx}: {str(e)}")
                        continue

        print(f"[DEBUG] Всего найдено видео: {len(videos)}")
        return videos
        
    except Exception as e:
        print(f"[ERROR] Ошибка при поиске видео: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


async def handle_video_search_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик запроса на поиск видео"""
    context.user_data["state"] = "searching_video"
    await update.message.reply_text(
        "🔍 Введите название видео для поиска на YouTube:",
    )


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

    try:
        # Запускаем поиск в отдельном потоке
        loop = asyncio.get_event_loop()
        videos = await loop.run_in_executor(executor, search_youtube_sync, search_query, 10)

        # Удаляем сообщение о поиске
        try:
            await status_message.delete()
        except:
            pass

        if not videos:
            # Если yt-dlp не нашел видео, показываем ссылку на YouTube поиск
            youtube_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
            
            text = f"""❌ Не удалось получить видео через встроенный поиск

🔍 Вот ссылка на поиск YouTube:
🔗 {youtube_search_url}

Или попробуйте другой поисковый запрос."""
            
            await update.message.reply_text(
                text,
                reply_markup=get_main_menu_keyboard(),
                disable_web_page_preview=False,
            )
            context.user_data["state"] = None
            return

        # Форматируем результаты
        text = f"🎥 Результаты поиска для: '{search_query}'\n\n"
        text += "Найдено видео:\n\n"

        for i, video in enumerate(videos, 1):
            # Форматируем длительность
            duration = video.get('duration', 0)
            if duration and isinstance(duration, (int, float)):
                try:
                    total_seconds = int(duration)
                    minutes = total_seconds // 60
                    seconds = total_seconds % 60
                    duration_str = f"{minutes}:{seconds:02d}"
                except (ValueError, TypeError):
                    duration_str = "?"
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

    except Exception as e:
        # Удаляем сообщение о поиске
        try:
            await status_message.delete()
        except:
            pass
        
        # Если ошибка, показываем ссылку на YouTube поиск
        youtube_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        
        text = f"""⚠️ Ошибка при поиске видео: {str(e)}

🔍 Вот ссылка на поиск YouTube:
🔗 {youtube_search_url}"""
        
        await update.message.reply_text(
            text,
            reply_markup=get_main_menu_keyboard(),
            disable_web_page_preview=False,
        )
    finally:
        context.user_data["state"] = None
