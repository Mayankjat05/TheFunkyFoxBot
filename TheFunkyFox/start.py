import os
import asyncio
from bot import Bot
from pyrogram import Client, filters, __version__, enums
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import OWNER_ID, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from TheFunkyFox.helper_func import subscribed, encode, decode, get_messages
from TheFunkyFox.database.sql import add_user, query_msg, full_userbase


# ---------------------- ᴛʜᴇ-ғᴜɴᴋʏ-ғᴏx-ʙᴏᴛ-ᴛᴇxᴛ ---------------------- #

WAIT_MSG = """"<b>ᴘʀᴏᴄᴇssɪɴɢ ...</b>"""

REPLY_ERROR = """<code>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ᴏᴜᴛ ᴀɴʏ sᴘᴀᴄᴇs.</code>"""

START_MSG = """
ʜᴇʟʟᴏ {first}\n
๏ ɪ ᴀᴍ ᴛʜᴇ ғᴜɴᴋʏ ғᴏx ᴀɴᴅ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs
๏ ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘᴏsᴛs ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛs ᴀɴᴅ ɪᴛ ᴄᴀɴ ᴀᴄᴄᴇss ʙʏ sᴘᴇᴄɪᴀʟ ʟɪɴᴋs 

๏ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏɴ ᴀʟʟ ᴛʜᴇ ʟᴀᴛᴇsᴛ ᴜᴘᴅᴀᴛᴇs.
"""

FORCE_MSG = """
ʜᴇʏ {first} \n
ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ʏᴇᴛ, ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ !
"""

# ---------------------- ᴛʜᴇ-ғᴜɴᴋʏ-ғᴏx-ʙᴏᴛ-ᴛᴇxᴛ ---------------------- #


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    user_name = '@' + message.from_user.username if message.from_user.username else None
    try:
        await add_user(id, user_name)
    except:
        pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION):
                caption = CUSTOM_CAPTION.format(file_caption = "" if not msg.caption else msg.caption.html)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍒 ᴜᴘᴅᴀᴛᴇs", url = "https://t.me/TheMoviesUpdate"),
                    InlineKeyboardButton("🔐 ᴀʙᴏᴜᴛ", callback_data = "about"),
                    InlineKeyboardButton("🍻 sᴜᴘᴘᴏʀᴛ", url = "https://t.me/TheMoviesRequests")
                ],
                [                    
                    InlineKeyboardButton("♻️ ᴄʟᴏsᴇ", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'ᴛʀʏ ᴀɢᴀɪɴ',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(OWNER_ID))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} | ᴜsᴇʀs ᴀʀᴇ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(OWNER_ID))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i> ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴇssᴀɢᴇ.. \nᴛʜɪs ᴡɪʟʟ ᴛᴀᴋᴇ sᴏᴍᴇ ᴛɪᴍᴇ</i>")
        for row in query:
            chat_id = int(row[0])
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                blocked += 1
            except InputUserDeactivated:
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>🍒 ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>

🔐 ᴛᴏᴛᴀʟ ᴜsᴇʀs ➠ <code>{total}</code>
🍻 sᴜᴄᴄᴇssғᴜʟʟ.➠ <code>{successful}</code>
🍒 ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ➠ <code>{blocked}</code>
♻️ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ➠ <code>{deleted}</code>
🐝 ᴜɴsᴜᴄᴄᴇssғᴜʟʟ ➠ <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
