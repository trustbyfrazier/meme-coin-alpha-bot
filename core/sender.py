import requests
from io import BytesIO
from core.logger import log, error_log

def send_message_with_image(bot, chat_id, message_text, image_url):
    try:
        # Just send the message with the image URL in the caption
        full_message = f"{message_text}\n{image_url}"
        bot.send_message(chat_id=chat_id, text=full_message, parse_mode='HTML')
        log("Message sent to Telegram successfully with image link.")
    except Exception as e:
        error_log(f"Failed to send message with image link: {e}")

