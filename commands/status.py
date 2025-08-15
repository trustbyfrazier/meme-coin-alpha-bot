import time
from core.logger import log

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{int(hours)}h {int(minutes)}m"

def send_status(bot, message, start_time, last_fetch_time):
    current_time = time.time()
    uptime_seconds = current_time - start_time
    uptime = format_duration(uptime_seconds)

    last_fetch = "N/A" if last_fetch_time is None else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_fetch_time))

    status_msg = (
        f"✅ <b>Bot Status</b>\n"
        f"Uptime: {uptime}\n"
        f"Last Fetch: {last_fetch}\n"
    )

    bot.send_message(chat_id=message.chat.id, text=status_msg, parse_mode='HTML')
    log("Sent /status response.")

