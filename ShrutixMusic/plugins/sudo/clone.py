from pyrogram import filters
from ShrutixMusic import app
from ShrutixMusic.core.clone_manager import start_clone, stop_clone
from ShrutixMusic.utils.database import set_clone_data
from config import SUDOERS

@app.on_message(filters.command("clone") & filters.user(SUDOERS))
async def clone_bot(_, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /clone <bot_token>")

    token = message.command[1]
    result = await start_clone(token)
    await message.reply(result)


@app.on_message(filters.command("rmbot") & filters.user(SUDOERS))
async def remove_bot(_, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /rmbot <bot_token>")

    token = message.command[1]
    result = await stop_clone(token)
    await message.reply(result)


@app.on_message(filters.command("setstartpic") & filters.user(SUDOERS))
async def set_start_pic(_, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("Reply to a photo.")

    token = message.command[1]
    file_id = message.reply_to_message.photo.file_id
    await set_clone_data(token, "start_pic", file_id)

    await message.reply("Start image set.")


@app.on_message(filters.command("setpingpic") & filters.user(SUDOERS))
async def set_ping_pic(_, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("Reply to a photo.")

    token = message.command[1]
    file_id = message.reply_to_message.photo.file_id
    await set_clone_data(token, "ping_pic", file_id)

    await message.reply("Ping image set.")


@app.on_message(filters.command("setstartcaption") & filters.user(SUDOERS))
async def set_caption(_, message):
    if len(message.command) < 3:
        return await message.reply("Usage: /setstartcaption <token> <caption>")

    token = message.command[1]
    caption = message.text.split(None, 2)[2]

    await set_clone_data(token, "start_caption", caption)

    await message.reply("Start caption updated.")
