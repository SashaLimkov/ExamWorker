import aioschedule as aioschedule
from asgiref.sync import async_to_sync

from bot.config.loader import bot


@async_to_sync
async def send_new_time(chat_id, text):
    await bot.send_message(
        chat_id=chat_id,
        text=text
    )

async def scheduler():
    aioschedule.every().day.at("17:45").do(choose_your_dinner)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)