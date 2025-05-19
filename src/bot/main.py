import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from .handlers import start, devops_handler, cafef_handler, vnexpress_handler

# Load biến môi trường
load_dotenv()

# Lấy token từ biến môi trường
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def main():
    """Khởi tạo và chạy bot"""
    # Khởi tạo application
    application = Application.builder().token(TOKEN).build()

    # Thêm các command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("devops", devops_handler))
    application.add_handler(CommandHandler("cafef", cafef_handler))
    application.add_handler(CommandHandler("vnexpress", vnexpress_handler))

    # Chạy bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main()) 