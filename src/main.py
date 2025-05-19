import asyncio
import logging
import sys
from telegram.ext import Application, CommandHandler
from bot.handlers import start, devops_handler, cafef_handler, vnexpress_handler
from bot.config import TELEGRAM_BOT_TOKEN

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Khởi tạo và chạy bot"""
    try:
        # Khởi tạo application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Thêm các command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("devops", devops_handler))
        application.add_handler(CommandHandler("cafef", cafef_handler))
        application.add_handler(CommandHandler("vnexpress", vnexpress_handler))

        # Chạy bot
        print("Bot đang chạy...")
        application.run_polling(drop_pending_updates=True)

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 