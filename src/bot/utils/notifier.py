
from asgiref.sync import async_to_sync

from bot.config.loader import bot


@async_to_sync
async def send_new_time(chat_id, text):
    await bot.send_message(
        chat_id=chat_id,
        text=text
    )