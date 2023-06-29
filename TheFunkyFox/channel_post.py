import asyncio
from bot import Bot
from pyrogram import filters, Client, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from TheFunkyFox.stats import get_shortlink
from config import OWNER_ID, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from TheFunkyFox.helper_func import encode


@Bot.on_message(filters.private & filters.user(OWNER_ID) & ~filters.command(['start','users','broadcast','batch','genlink']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ...!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("♻️ ʜᴇʀᴇ ɪs ʏᴏᴜʀ sʜᴏʀᴛ ʟɪɴᴋ ♻️", url=await get_shortlink(f'{link}')]])

    await reply_text.edit(f"<b>ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("♻️ ᴄᴏᴘʏ ᴜʀʟ ♻️", url=f'{link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
