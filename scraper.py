# /usr/bin/nuhmanpk/bughunter0 

import asyncio
import time
import requests
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils import REPO
from helpers import (
    download_media,
    progress_bar,
    progress_for_pyrogram
)
import imageio
from tqdm import tqdm


async def scrape(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html5lib")
        return request, soup
    except Exception as e:
        print(e)
        return None, None








    


async def all_video_scraping(bot,query):
    try:
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)

        video_tags = soup.find_all("video")

        video_links = [
            video["src"] if video.has_attr("src") else video.find("source")["src"]
            for video in video_tags
        ]

        txt = await txt.edit(
            text=f"Found {len(video_links)} Videos", disable_web_page_preview=True
        )

        if len(video_links):
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-videos"
            os.makedirs(folder_name, exist_ok=True)

            for idx, video_link in enumerate(video_links):
                progress, percentage = await progress_bar(idx + 1, len(video_links))

                try:
                    await status.edit(
                        f"Downloading...{idx + 1}/{len(video_links)}\nPercentage: {percentage}%\nProgress: {progress}\n"
                    )
                except:
                    pass
                video_data, local_filename = await download_media(
                    message.text, video_link, idx, "video"
                )

                if video_data:
                    with open(os.path.join(folder_name, local_filename), "wb") as file:
                        file.write(video_data)

                time.sleep(0.3)

            await status.edit("Uploading ....")
            zip_filename = f"{folder_name}.zip"
            shutil.make_archive(folder_name, "zip", folder_name)

            c_time = time.time()
            await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
            await message.reply_document(
                open(zip_filename, "rb"),
                caption="Here are the videos! \n @BughunterBots",
                progress=progress_for_pyrogram,
                progress_args=('Uploading',status,c_time)  
            )
            # await message.reply_video(local_filename)
            await status.delete()
            await txt.delete()
            shutil.rmtree(folder_name)
            await asyncio.sleep(1)
            os.remove(zip_filename)
            return

        else:
            await txt.edit(text=f"No Videos Found!!!", disable_web_page_preview=True)
            return

    except Exception as e:
        print(e)
        os.remove(zip_filename)
        error = f"ERROR: {(str(e))}"
        error_link = f"{REPO}/issues/new?title={quote(error)}"
        text = f"Something Bad occurred !!!\nCreate an issue here"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]]
        )
        await message.reply_text(
            text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup
        )
        return e



###################

