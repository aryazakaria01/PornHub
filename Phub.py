import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download
from config import OWNER, BOT_NAME, REPO_BOT, ARQ_API_KEY, UPDATES_CHANNEL, TOKEN
# Config Check-----------------------------------------------------------------

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://arq.hamker.in", ARQ_API_KEY, session)
pornhub = arq.pornhub
phdl = arq.phdl

app = Client(f"{BOT_NAME}", bot_token=f"{TOKEN}", api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")
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
@app.on_message(
    filters.command("start") & ~filters.edited
)
async def start(_, message):
    m= await message.reply_text(
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
@app.on_message(
    filters.command("help") & ~filters.edited
)
async def help(_, message):
    await message.reply_text(
        """**🛠 available command:**
        
/help see the help message.\n
/repo get the repo link.\n
If you want to download phub video, just type any query."""
    )
    
# Repo  -----------------------------------------------------------------------
@app.on_message(
    filters.command("repo") & ~filters.edited
)
async def repo(_, message):
    m= await message.reply_text(
        text="""Great, you can make your own bot now, tap the button below to get the repository link.""",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("🧩 REPO 🧩", url=f"{REPO_BOT}"),
              InlineKeyboardButton("👩‍💻 OWNER 👩‍💻", url=f"t.me/{OWNER}")
              
              ]
            ]
          )
       )

# Let's Go----------------------------------------------------------------------
@app.on_message(
    filters.private & ~filters.edited & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo")
    )
async def sarch(_,message):
    try:
        if "/" in message.text.split(None,1)[0]:
            await message.reply_text(
                "**💡 usage:**\njust type the phub video name you want to download, and this bot will send you the result."
            )
            return
    except:
        pass
    m = await message.reply_text("getting results...")
    search = message.text
    try:
        resp = await pornhub(search,thumbsize="large")
        res = resp.result
    except:
        await m.edit("not found: 404")
        return
    if not resp.ok:
        await m.edit("not found, try again")
        return
    resolt = f"""
**🏷 TITLE:** {res[0].title}
**⏰ DURATION:** {res[0].duration}
**👁‍🗨 VIEWERS:** {res[0].views}
**🌟 RATING:** {res[0].rating}"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload")
                ]
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("◀️ PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload"),
                ],
                [
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("◀️ PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload")
                ]
              ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[curr_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("◀️ PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("📥DOWNLOAD",
                                         callback_data="dload")
                ]
            ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[curr_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
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
    resolt = f"""
**🏷 TITLE:** {res[curr_page].title}
**⏰ DURATION:** {res[curr_page].duration}
**👁‍🗨 VIEWERS:** {res[curr_page].views}
**🌟 RATING:** {res[curr_page].rating}"""
    pos = 1
    cbb = []
    for resolts in dl_links.result.video:
        b= [InlineKeyboardButton(f"{resolts.quality} - {resolts.size}", callback_data=f"phubdl {pos}")]
        pos += 1
        cbb.append(b)
    cbb.append([InlineKeyboardButton("Delete", callback_data="delete")])
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button 2--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex(r"^phubdl"))
async def callback_query_dl(_, query):
    m = query.message
    capsion = m.caption
    entoty = m.caption_entities
    await m.edit(f"**downloading...** :\n\n{capsion}")
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    thomb = await download_url(data['thumb'])
    durr = await time_to_seconds(data['dur'])
    pos = int(query.data.split()[1])
    pos = pos-1
    try:
        vid = await download_url(res[pos].url)
    except Exception as e:
        print(e)
        await m.edit("download error..., try again")
        return
    await m.edit(f"**Upload Sekarang** :\n\n{capsion}")
    await app.send_chat_action(m.chat.id, "upload_video")
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
