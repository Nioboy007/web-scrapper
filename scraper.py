# /usr/bin/nuhmanpk/bughunter0 

import asyncio
import time
import shutil
import requests
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils import REPO
from helpers import (
    progress_bar,
    progress_for_pyrogram
)


async def scrape(url):
    try:
        print("scrape fnc started")
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html5lib")
        return request, soup
    except Exception as e:
        print(e)
        return None, None
        print("scrape fnc finished")


async def all_video_scraping(bot,query):
    try:
        print("all video scraping started")
        message = query.message
        chat_id = message.chat.id
        txt = await message.reply_text("Scraping url ...", quote=True)
        request, soup = await scrape(message.text)
        print("all video scraping: phase 1")

        video_tags = soup.find_all("video")

        video_links = [
            video["src"] if video.has_attr("src") else video.find("source")["src"]
            for video in video_tags
        ]
        print("all video scraping phase 2")

        txt = await txt.edit(
            text=f"Found {len(video_links)} Videos", disable_web_page_preview=True
        )
        print("all video scraping 2.1")

        if len(video_links):
            status = await message.reply_text("Checking...", quote=True)
            folder_name = f"{message.chat.id}-videos"
            os.makedirs(folder_name, exist_ok=True)
            print("all video scraping 2.2")

            for idx, video_link in enumerate(video_links):
                progress, percentage = await progress_bar(idx + 1, len(video_links))

                try:
                    await status.edit(
                        f"Downloading...{idx + 1}/{len(video_links)}\nPercentage: {percentage}%\nProgress: {progress}\n"
                    )
                    print("all video scraping 2.3")
                except:
                    pass
                video_data, local_filename = await download_media(
                    message.text, video_link, idx, "video"
                )
                print("all video scraping: phase 3")

                if video_data:
                    with open(os.path.join(folder_name, local_filename), "wb") as file:
                        file.write(video_data)

                time.sleep(0.3)
                print("all video scraping: phase 4")

            await status.edit("Uploading ....")
            zip_filename = f"{folder_name}.zip"
            shutil.make_archive(folder_name, "zip", folder_name)
            print("all video scraping: phase 5")

            c_time = time.time()
            await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
            await message.reply_document(
                open(zip_filename, "rb"),
                caption="Here are the videos! \n @BughunterBots",
                progress=progress_for_pyrogram,
                progress_args=('Uploading',status,c_time)  
            )
            print("all video scraping: vid sent")
            # await message.reply_video(local_filename)
            await status.delete()
            await txt.delete()
            shutil.rmtree(folder_name)
            await asyncio.sleep(1)
            os.remove(zip_filename)
            return
            print("all video scraping finished")

        else:
            await txt.edit(text=f"No Videos Found!!!", disable_web_page_preview=True)
            return

    except Exception as e:
        print(e)
        os.remove(zip_filename)
        error = f"ERROR: {(str(e))}"
        return e



async def download_media(base_url, media_url, idx, media_type):
    try:
        with requests.get(media_url, stream=True) as response:
            response.raise_for_status()
            print("Download media phase: 1 ")

            filename = os.path.basename(media_url)
            local_filename = f"{media_type}{idx}_{filename}"
            print("Download media phase:  2 ") 

            with open(local_filename, "wb") as file:
                shutil.copyfileobj(response.raw, file)
                print("Download media phase:3 ")

            with open(local_filename, "rb") as file:
                media_data = file.read()
                print("Download media phase: 4 ")

            os.remove(local_filename)
            return media_data, local_filename
    except Exception as e:
        print(f"Error downloading media from {media_url}: {e}")
        return None 

