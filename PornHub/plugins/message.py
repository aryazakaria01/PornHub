from typing import Union
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from ..config import prefixs, sub_chat, sudoers


sudofilter = filters.user(sudoers)

button_a1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="✅ Agree & Continue",
                callback_data="final_page",
            )
        ],[
            InlineKeyboardButton(
                text="❌ Cancel",
                callback_data="home_intro",
            ),
        ],
    ]
)


button_a2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Search here", switch_inline_query_current_chat="",
            )
        ],[
            InlineKeyboardButton(
                text="Search in chat", switch_inline_query="",
            ),
        ],
    ]
)


@Client.on_message(filters.command(["start", "restart"], prefixs) & filters.private)
async def intro_msg(_, update: Message):
    match = str(update.chat.id)
    with open("users.txt", "a+") as file:
        file.seek(0)
        line = file.read().splitlines()
        if match in line:
            print(f"User {match} is using the bot")
        else:
            file.write(match + "\n")
    
    method = update.reply_text
    text = f"👋🏻 Hi {update.from_user.first_name}!\n\nUse this bot to download videos from the pornhub.com site by providing the name of the video you want to download or you can also search for the video you want to download via inline mode.\n\n💭 Join the redirected channel in order to use this bot!"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Channel •", url=f"https://t.me/{sub_chat}",
                )
            ],[
                InlineKeyboardButton(
                    "Terms of use & Privacy", callback_data="terms",
                ),
            ],
        ]
    )
    await method(text, reply_markup=button)


@Client.on_callback_query(filters.regex("^home_intro$"))
async def home_page(_, update: CallbackQuery):
    await update.answer("Accept the policy in order to continue!")
    method = update.edit_message_text
    text = f"👋🏻 Hi {update.from_user.first_name}!\n\nUse this bot to download videos from the pornhub.com site by providing the name of the video you want to download or you can also search for the video you want to download via inline mode.\n\n💭 Join the redirected channel in order to use this bot!"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Channel •", url=f"https://t.me/{sub_chat}",
                )
            ],[
                InlineKeyboardButton(
                    "Terms of use & Privacy", callback_data="terms",
                ),
            ],
        ]
    )
    await method(text, reply_markup=button)


@Client.on_callback_query(filters.regex("^terms$"))
async def terms_panel(_, q: CallbackQuery):
    await q.answer("Read the terms of use & user privacy!")
    text = """
🧸 <u><b>PornHub bot</b></u>
⚠️ <b>WARNING !</b>
This bot contains 18+ content, make sure you are an adult user to be able to use this bot!. Reporting this bot will get it blocked by Telegram, so if you're considering sticking with bots, don't do it!
🔐 <b>Privacy Policy</b>
We ensure that your search data in this bot is protected safely.  Whoever you are, whenever and wherever you use this bot to download videos from pornhub, you don't have to be afraid of spreading it to the public.
<i>You don't have to worry, because our bot staff will make sure that your data is well protected and safe.</i>
👉🏻 Press the <b>green button</b> to declare that you have <b>read and accepted these conditions</b> to use this bot, otherwise cancel.
    """
    await q.edit_message_text(text, reply_markup=button_a1)


@Client.on_callback_query(filters.regex("^final_page$"))
async def greets(_, q: CallbackQuery):
    await q.answer("Thanks for agreeing to the bot policy!")
    await q.edit_message_text(
        f"Hi {q.from_user.first_name}!\n\nYou can browse this bot now, just tap one of the button below and enter any name of the video you want to download.",
        reply_markup=button_a2,
    )


@Client.on_message(filters.command("stats", prefixs) & sudofilter)
async def bot_statistic(c: Client, u: Message):
    users = open("users.txt").readlines()
    total = len(users)
    await c.send_document(
        u.chat.id,
        "users.txt", caption=f"total: {total} users",
    )


@Client.on_message(filters.command(["gcast", "broadcast"], prefixs) & sudofilter)
async def broadcast(_, update: Message):
    if not update.reply_to_message:
        await update.reply_text("Reply to message for broadcast!")
        return
    if update.reply_to_message.text:
        await update.reply_text("✅ Broadcast success!")
        query = open("users.txt").readlines()
        for row in query:
            try:
                resp = update.reply_to_message
                await resp.copy(row)
            except Exception:
                pass
    else:
        await update.reply_text("Other message type like sticker, photo, etc; are not supported!")


@Client.on_message(filters.command("help", prefixs))
async def command_list(_, update: Message):
    text_1 = """
🛠 Command list:
» /start - start this bot
» /help  - showing this message
» /ping  - check bot status
    """
    text_2 = """
🛠 Command list:
» /start - start this bot
» /help  - showing this message
» /ping  - check bot status
» /stats - show bot statistic
» /gcast - broadcast message
    """
    if update.from_user.id in sudoers:
        await update.reply_text(text_2)
    else:
        await update.reply_text(text_1)


@Client.on_message(filters.command("ping", prefixs))
async def ping(c: Client, u: Message):
    first = datetime.now()
    sent = await u.reply_text("<b>pinging...</b>")
    second = datetime.now()
    await sent.edit_text(
       f"🏓 <b>PONG !</b>\n⏱ <code>{(second - first).microseconds / 1000}</code> ms"
    )
