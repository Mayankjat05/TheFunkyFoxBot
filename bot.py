import os
import sys
import config
import pyromod.listen
from pyrogram import Client, enums
from pyrogram.enums import ParseMode
from datetime import datetime
from config import LOGGER, FORCE_SUB_CHANNEL, CHANNEL_ID


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="TheFunkyFox",
            api_hash=config.API_HASH,
            api_id=config.API_ID,
            plugins={
                "root": "TheFunkyFox"
            },
            workers=config.BOT_WORKERS,
            bot_token=config.BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("» ʙᴏɴᴛ ᴄᴀɴ'ᴛ ᴇxᴘᴏʀᴛ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ғʀᴏᴍ ғᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ !")
                self.LOGGER(__name__).warning(f"ᴘʟᴇᴀsᴇ ᴅᴏᴜʙʟᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ FORCE_SUB_CHANNEL ᴠᴀʟᴜᴇ ᴀɴᴅ ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ᴄʜᴀɴɴᴇʟ ᴡɪᴛʜ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ᴘᴇʀᴍɪssɪᴏɴ, ᴄᴜʀʀᴇɴᴛ ғᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ ᴠᴀʟᴜᴇ: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\n••• ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ •••")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ᴅʙ ᴄʜᴀɴɴᴇʟ, ᴀɴᴅ ᴅᴏᴜʙʟᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ CHANNEL_ID ᴠᴀʟᴜᴇ, ᴄᴜʀʀᴇɴᴛ ᴠᴀʟᴜᴇ {CHANNEL_ID}")
            self.LOGGER(__name__).info("\n••• ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ •••")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴘʟᴏʏᴇᴅ 🍎")
        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("••• ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ •••")
