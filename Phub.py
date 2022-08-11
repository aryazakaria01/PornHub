import os

from wget import download
from Python_ARQ import ARQ
from aiohttp import ClientSession
from asyncio import get_running_loop
from pyrogram import filters, Client
from pyrogram.enums import ParseMode
from pyrogram.enums.chat_action import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from config import OWNER, BOT_NAME, REPO_BOT, ARQ_API_KEY, UPDATES_CHANNEL, TOKEN

# Config Check-----------------------------------------------------------------


# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://arq.hamker.in", ARQ_API_KEY, session)
pornhub = arq.pornhub
phdl = arq.phdl

app = Client(
    name="PornHubBot", 
    bot_token=TOKEN, 
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
)
print("\n✨ BOT IS READY TO USE ✨\n")


db = {}


async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file


async def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )


# Start  -----------------------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(_, message):
    m = await app.send_message(
        message.chat.id,
        text=f"🇬🇧 Hello, i'm {BOT_NAME}. you can download pornhub video with the quality up to 1080p, Just type a query or the video name you want to download and the bot will send you the result!\n\n🇮🇩 Halo, saya {BOT_NAME}, anda dapat mengunduh video dari pornhub dengan kualitas tinggi sampai 1080p, berikan saja nama/judul video yang ingin anda unduh maka saya akan memberikan hasil nya kepada anda.",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("📣 Updates Channel", url=f"t.me/{UPDATES_CHANNEL}")
            ]
          ]
        )
    )


# Help-------------------------------------------------------------------------
@app.on_message(filters.command("help"))
async def help(_, message):
    await app.send_message(
        message.chat.id,
        """**🛠 available command:**
        
/help see the help message.\n
/repo get the repo link.\n
If you want to download phub video, just type any query."""
    )

    
# Repo  -----------------------------------------------------------------------
@app.on_message(filters.command("repo"))
async def repo(_, message):
    m= await app.send_message(
        message.chat.id,
        text="""Great, you can make your own bot now, tap the button below to get the repository link.""",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("Repo", url=f"{REPO_BOT}"),
              InlineKeyboardButton("Owner", url=f"t.me/{OWNER}")
              
              ]
            ]
          )
       )


# Let's Go----------------------------------------------------------------------
@app.on_message(
    filters.private & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo")
    )
async def sarch(_,message):
    try:
        if "/" in message.text.split(None,1)[0]:
            await app.send_message(
                message.chat.id,
                "**💡 usage:**\njust type the phub video name you want to download, and this bot will send you the result."
            )
            return
    except Exception:
        pass
    m = await app.send_message(message.chat.id, "Getting results...")
    search = message.text
    try:
        resp = await pornhub(search,thumbsize="large")
        res = resp.result
    except Exception:
        await m.edit("Not found: 404")
        return
    if not resp.ok:
        await m.edit("Not found, try again")
        return
    resolt = (
          f"**🏷 Title:** {res[0].title}"
          f"**⏱️ Duration:** {res[0].duration}"
          f"**👀 Viewers:** {res[0].views}"
          f"**🌟 Rating:** {res[0].rating}"
    )
    await m.delete()
    m = await app.send_photo(
        message.chat.id,
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▶️ Next", callback_data="next"),
                    InlineKeyboardButton("🗑 Delete", callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("📥 Download", callback_data="dload")
                ]
            ]
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db


# Next Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except Exception:
        await m.edit("Something went wrong, try again later")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("◀️ Back", callback_data="previous"),
                    InlineKeyboardButton("📥 Download", callback_data="dload"),
                ],
                [
                    InlineKeyboardButton("🗑 Delete", callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("◀️ Back", callback_data="previous"),
                    InlineKeyboardButton("▶️ Next", callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 Delete", callback_data="delete"),
                    InlineKeyboardButton("📥 Download", callback_data="dload")
                ]
              ]
    resolt = (
          f"**🏷️ Title:** {res[cur_page].title}"
          f"**⏱️ Duration:** {res[curr_page].duration}"
          f"**👀 Viewers:** {res[cur_page].views}"
          f"**🌟 Rating:** {res[cur_page].rating}"
    )
    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode=ParseMode.MARKDOWN,
    )


# Previous Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except Exception:
        await m.edit("Something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("◀️ Back", callback_data="previous"),
                    InlineKeyboardButton("▶️ Next", callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 Delete", callback_data="delete"),
                    InlineKeyboardButton("📥 Download", callback_data="dload")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("▶️ Next", callback_data="next"),
                    InlineKeyboardButton("🗑 Delete", callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("📥 Download", callback_data="dload")
                ]
            ]
    resolt = (
          f"**🏷 Title:** {res[cur_page].title}"
          f"**⏱ Duration:** {res[curr_page].duration}"
          f"**👀 Viewers:** {res[cur_page].views}"
          f"**🌟 Rating:** {res[cur_page].rating}"
    )
    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode=ParseMode.MARKDOWN,
    )


# Download Button--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex("dload"))
async def callback_query_next(_, query):
    m = query.message
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    dl_links = await phdl(res[curr_page].url)
    db[m.chat.id]['result'] = dl_links.result.video
    db[m.chat.id]['thumb'] = res[curr_page].thumbnails[0].src
    db[m.chat.id]['dur'] = res[curr_page].duration
    cbb = []
    resolt = (
          f"**🏷 Title:** {res[curr_page].title}"
          f"**⏱ Duration:** {res[curr_page].duration}"
          f"**👀 Viewers:** {res[curr_page].views}"
          f"**🌟 Rating:** {res[curr_page].rating}"
    )
    for pos, resolts in enumerate(dl_links.result.video, start=1):
        b= [InlineKeyboardButton(f"{resolts.quality} - {resolts.size}", callback_data=f"phubdl {pos}")]
        cbb.append(b)
    cbb.append([InlineKeyboardButton("Delete", callback_data="delete")])
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode=ParseMode.MARKDOWN,
    )


# Download Button 2--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex(r"^phubdl"))
async def callback_query_dl(_, query):
    m = query.message
    capsion = m.caption
    entoty = m.caption_entities
    await m.edit(f"**Downloading...** :\n\n{capsion}")
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    thomb = await download_url(data['thumb'])
    durr = await time_to_seconds(data['dur'])
    pos = int(query.data.split()[1]) - 1
    try:
        vid = await download_url(res[pos].url)
    except Exception as e:
        print(e)
        await m.edit("Download error, try again later")
        return
    await m.edit(f"**Uploading the file** :\n\n{capsion}")
    await app.send_chat_action(m.chat.id, ChatAction.UPLOAD_VIDEO)
    await m.edit_media(media=InputMediaVideo(vid,thumb=thomb, duration=durr, supports_streaming=True))
    await m.edit_caption(caption=capsion, caption_entities=entoty)
    if os.path.isfile(vid):
        os.remove(vid)
    if os.path.isfile(thomb):
        os.remove(thomb)


# Delete Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, query):
    await query.message.delete()


app.run()
