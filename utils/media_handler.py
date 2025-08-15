import requests
from io import BytesIO
from core.logger import log, error_log

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        log(f"Image downloaded from {url}")
        return BytesIO(response.content)
    except Exception as e:
        error_log(f"Failed to download image from {url}: {e}")
        return None

def send_image(bot, chat_id, image_data, caption):
    try:
        bot.send_photo(chat_id=chat_id, photo=image_data, caption=caption, parse_mode='HTML')
        log("Image sent via file upload.")
    except Exception as e:
        error_log(f"Failed to send image: {e}")

