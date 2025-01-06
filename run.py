import threading
from backend.main import app
from backend.telegram_bot import run_bot
import uvicorn

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_telegram_bot():
    run_bot()

if __name__ == "__main__":
    # Запуск FastAPI в отдельном потоке
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    # Запуск Telegram-бота
    run_telegram_bot()