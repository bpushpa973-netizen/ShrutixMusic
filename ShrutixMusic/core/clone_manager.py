from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH
from ShrutixMusic.utils.database import (
    add_clone, remove_clone, get_clones,
    set_clone_data, get_clone_data
)

CLONED_BOTS = {}

async def start_clone(token: str):

    if token in CLONED_BOTS:
        return "Already running."

    bot = Client(
        name=f"clone_{token[:8]}",
        bot_token=token,
        api_id=API_ID,
        api_hash=API_HASH,
    )

    # START
    @bot.on_message(filters.command("start"))
    async def start_handler(client, message):
        photo = await get_clone_data(token, "start_pic")
        caption = await get_clone_data(token, "start_caption") or "Hello! I am cloned bot."

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("⚙ Clone Settings", callback_data="clone_settings")]]
        )

        if photo:
            await message.reply_photo(photo, caption=caption, reply_markup=button)
        else:
            await message.reply(caption, reply_markup=button)

    # PING
    @bot.on_message(filters.command("ping"))
    async def ping_handler(client, message):
        photo = await get_clone_data(token, "ping_pic")

        if photo:
            await message.reply_photo(photo, caption="🏓 Pong!")
        else:
            await message.reply("🏓 Pong!")

    await bot.start()
    CLONED_BOTS[token] = bot
    await add_clone(token)

    return "Clone started successfully."

async def stop_clone(token: str):

    if token not in CLONED_BOTS:
        return "Bot not running."

    await CLONED_BOTS[token].stop()
    del CLONED_BOTS[token]
    await remove_clone(token)

    return "Clone stopped successfully."

async def load_clones():
    async for data in get_clones():
        await start_clone(data["token"])
