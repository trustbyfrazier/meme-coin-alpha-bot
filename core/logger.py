from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def error_log(message):
    print(f"[ERROR {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

