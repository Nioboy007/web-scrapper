import shutil
import requests
from utils import FINISHED_PROGRESS_STR, UN_FINISHED_PROGRESS_STR
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
import math
import os
import time


async def progress_bar(current, total):
    percentage = current / total
    finished_length = int(percentage * 10)
    unfinished_length = 10 - finished_length
    progress = f"{FINISHED_PROGRESS_STR * finished_length}{UN_FINISHED_PROGRESS_STR * unfinished_length}"
    formatted_percentage = "{:.2f}".format(percentage * 100)
    return progress, formatted_percentage


async def progress_for_pyrogram(current, total, ud_type, message, start):
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚫Cancel", callback_data="cdstoptrasmission")]]
    )
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n <b>📊Percentage:</b> {2}%\n".format(
            "".join(["■" for i in range(math.floor(percentage / 5))]),
            "".join(["□" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = (
            progress
            + "<b>✅Completed:</b>{0} \n<b>📁Total Size:</b> {1}\n<b>🚀Speed:</b> {2}/s\n<b>⌚️ETA:</b> {3}\n @BughunterBots".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                estimated_total_time if estimated_total_time != "" else "0 s",
            )
        )
        try:
            await message.edit(
                text="{}\n {}".format(ud_type, tmp), reply_markup=reply_markup
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]





async def download_media(base_url, media_url, idx, media_type):
    try:
        with requests.get(media_url, stream=True) as response:
            response.raise_for_status()

            filename = os.path.basename(media_url)
            local_filename = f"{media_type}{idx}_{filename}"

            with open(local_filename, "wb") as file:
                shutil.copyfileobj(response.raw, file)

            with open(local_filename, "rb") as file:
                media_data = file.read()

            os.remove(local_filename)
            return media_data, local_filename
    except Exception as e:
        print(f"Error downloading media from {media_url}: {e}")
        return None


