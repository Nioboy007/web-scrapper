import os
from pyrogram import Client, filters
from dotenv import load_dotenv
import os
from pyrogram.types import Message
from scraper import all_video_scraping
from crawler import crawl_web
from utils import OPTIONS, START_BUTTON, START_TEXT

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

CRAWL_LOG_CHANNEL = os.getenv('CRAWL_LOG_CHANNEL')

if bot_token is None or api_id is None or api_hash is None:
    raise ValueError(
        "Please set the BOT_TOKEN, API_ID, and API_HASH environment variables."
    )

app = Client(
    "WebScrapperBot", bot_token=bot_token, api_id=int(api_id), api_hash=api_hash
)


@app.on_message(filters.command(["start"]))
async def start(_, message: Message):
    # Edit Your Start string here
    text = START_TEXT
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)


@app.on_callback_query()
async def cb_data(bot:Client, update):
    if update.data == "cballvideo":
        await all_video_scraping(bot,update)
    else:
        await update.message.reply('You must provide a Log Channel ID')


@app.on_message(
    (filters.regex("https") | filters.regex("http") | filters.regex("www"))
    & filters.private
)
async def scrapping(bot, message):
    await send_message_with_options(message)


async def send_message_with_options(message):
    reply_markup = OPTIONS
    await message.reply_text("Choose an Option")
    await message.reply_text(
        message.text, reply_markup=reply_markup, disable_web_page_preview=True
    )


# Use soup.find_all('tag_name') to Extract Specific Tag Details
"""
soup.title
# <title>This is Title</title>

soup.title.name
# u'title'

soup.title.string
# u'This is a string'

soup.title.parent.name
# u'head'
"""

app.run(print("Bot Running...."))
