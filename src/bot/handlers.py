import asyncio
import re
import requests
import cohere
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ContextTypes
from scrapers.news_scrapers import (
    get_html_links_from_url,
    get_devops_content,
    get_cafef_content,
    get_vnexpress_content
)
from .utils import split_message, summarize_text
from .config import COHERE_API_KEY, COHERE_MODEL

# Dictionary để lưu trữ link của người dùng
user_links = {}

async def process_article(update: Update, context: ContextTypes.DEFAULT_TYPE, content: str, article_url: str = None):
    """Xử lý và tóm tắt nội dung bài viết"""
    try:
        if not content:
            await update.message.reply_text("Không thể lấy nội dung bài viết.")
            return

        # Khởi tạo Cohere client
        co = cohere.Client(COHERE_API_KEY)
        
        # Tóm tắt nội dung
        summary_response = co.chat(
            model=COHERE_MODEL,
            message="Tóm tắt nội dung bài báo sau trong 200-300 từ: " + content
        )

        # Tạo thông báo
        message = f"""🔗 Link bài viết: {article_url}

📝 TÓM TẮT:
{summary_response.text}"""

        # Chia nhỏ nếu thông báo quá dài
        parts = split_message(message)
        for part in parts:
            await update.message.reply_text(part)
            await asyncio.sleep(0.5)  # Delay để tránh rate limit
            
    except Exception as e:
        print(f"Lỗi khi xử lý bài viết: {str(e)}")
        await update.message.reply_text(f"Có lỗi xảy ra: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start"""
    welcome_message = (
        "Chào mừng bạn đến với News Bot!\n\n"
        "Các lệnh có sẵn:\n"
        "/devops - Lấy bài viết từ devops.vn\n"
        "/cafef - Lấy bài viết từ cafef.vn\n"
        "/vnexpress - Lấy bài viết từ vnexpress.net\n\n"
        "Cách sử dụng:\n"
        "1. Gõ lệnh để lấy bài viết đầu tiên\n"
        "2. Gõ lệnh + số để lấy bài viết theo số thứ tự\n"
        "3. Gõ lệnh + link để phân tích bài viết cụ thể"
    )
    await update.message.reply_text(welcome_message)

async def devops_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /devops"""
    try:
        # Lấy tham số từ người dùng
        args = context.args
        user_id = update.effective_user.id
        
        # Nếu không có tham số, lấy bài viết đầu tiên từ trang chủ
        if not args:
            links = await get_html_links_from_url("https://devops.vn")
            if not links:
                await update.message.reply_text("Không tìm thấy bài viết nào.")
                return
            article_url = links[0]
            content = await get_devops_content(article_url)
            if not content:
                await update.message.reply_text("Không thể lấy nội dung bài viết.")
                return
            await process_article(update, context, content, article_url)
            return
            
        # Nếu có tham số là số
        if args[0].isdigit():
            index = int(args[0]) - 1
            links = await get_html_links_from_url("https://devops.vn")
            if not links:
                await update.message.reply_text("Không tìm thấy bài viết nào.")
                return
            if index < 0 or index >= len(links):
                await update.message.reply_text(f"Số bài viết không hợp lệ! Chỉ có {len(links)} bài viết.")
                return
            article_url = links[index]
            content = await get_devops_content(article_url)
            if not content:
                await update.message.reply_text("Không thể lấy nội dung bài viết.")
                return
            await process_article(update, context, content, article_url)
            return
            
        # Nếu tham số là URL
        article_url = args[0]
        if not article_url.startswith('https://devops.vn/'):
            await update.message.reply_text("Link không hợp lệ. Vui lòng nhập link từ devops.vn")
            return
            
        content = await get_devops_content(article_url)
        if not content:
            await update.message.reply_text("Không thể lấy nội dung bài viết.")
            return
        await process_article(update, context, content, article_url)
        
    except Exception as e:
        print(f"Lỗi trong devops_handler: {str(e)}")
        await update.message.reply_text(f"Có lỗi xảy ra: {str(e)}")

async def cafef_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /cafef"""
    try:
        # Lấy tham số từ người dùng
        args = context.args
        user_id = update.effective_user.id
        
        # Lấy danh sách link nếu chưa có
        if user_id not in user_links:
            links = await get_html_links_from_url("https://cafef.vn")
            user_links[user_id] = links
        
        if not user_links[user_id]:
            await update.message.reply_text("Không tìm thấy bài viết nào từ cafef.vn.")
            return
        
        if not args:
            # Lấy bài viết đầu tiên
            article_url = user_links[user_id][0]
            content = await get_cafef_content(article_url)
            await process_article(update, context, content, article_url)
        elif args[0].isdigit():
            # Lấy bài viết theo số
            index = int(args[0]) - 1
            if 0 <= index < len(user_links[user_id]):
                article_url = user_links[user_id][index]
                content = await get_cafef_content(article_url)
                await process_article(update, context, content, article_url)
            else:
                await update.message.reply_text(f"Số bài viết không hợp lệ! Chỉ có {len(user_links[user_id])} bài viết.")
        else:
            # Phân tích link cụ thể
            article_url = args[0]
            content = await get_cafef_content(article_url)
            await process_article(update, context, content, article_url)
        
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {str(e)}")

async def vnexpress_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /vnexpress"""
    try:
        # Lấy tham số từ người dùng
        args = context.args
        user_id = update.effective_user.id
        
        # Lấy danh sách link nếu chưa có
        if user_id not in user_links:
            links = await get_html_links_from_url("https://vnexpress.net")
            user_links[user_id] = links
        
        if not user_links[user_id]:
            await update.message.reply_text("Không tìm thấy bài viết nào từ vnexpress.net.")
            return
        
        if not args:
            # Lấy bài viết đầu tiên
            article_url = user_links[user_id][0]
            content = await get_vnexpress_content(article_url)
            await process_article(update, context, content, article_url)
        elif args[0].isdigit():
            # Lấy bài viết theo số
            index = int(args[0]) - 1
            if 0 <= index < len(user_links[user_id]):
                article_url = user_links[user_id][index]
                content = await get_vnexpress_content(article_url)
                await process_article(update, context, content, article_url)
            else:
                await update.message.reply_text(f"Số bài viết không hợp lệ! Chỉ có {len(user_links[user_id])} bài viết.")
        else:
            # Phân tích link cụ thể
            article_url = args[0]
            content = await get_vnexpress_content(article_url)
            await process_article(update, context, content, article_url)
        
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {str(e)}")

# Hàm lấy và tóm tắt bài báo theo thứ tự n
def get_summary_by_index(n):
    try:
        # B1: Truy cập trang chủ
        url = 'https://vnexpress.net/'
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # B2: Tìm danh sách link .html
        news_items = soup.find_all('a')
        html_links = []
        for item in news_items:
            link = item.get('href', '')
            if link.endswith('.html') and link.startswith('http'):
                html_links.append(link)

        if not html_links:
            return "Không tìm thấy bài báo nào."

        if n >= len(html_links):
            return f"Không tìm thấy bài báo thứ {n}. Chỉ có {len(html_links)} bài báo."

        article_url = html_links[n]

        # B3: Truy cập bài viết
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        cleaned_text = re.sub(r'\n+', '\n', article_soup.text)

        # B4: Tóm tắt với Cohere
        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            model=COHERE_MODEL,
            message="Tóm tắt nội dung bài báo sau trong 300-400 từ: " + cleaned_text
        )

        return f"Tóm tắt bài báo thứ {n} ({article_url}):\n\n{response.text}"

    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

# /start – lấy bài đầu tiên
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Đang tóm tắt bài báo đầu tiên...")
    summary = get_summary_by_index(0)
    await update.message.reply_text(summary)

# /new n – lấy bài thứ n
async def new_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) == 0:
            await update.message.reply_text("Bạn cần nhập số bài báo. Ví dụ: /new 3")
            return

        n = int(context.args[0])
        await update.message.reply_text(f"Đang tóm tắt bài báo thứ {n}...")
        summary = get_summary_by_index(n)
        await update.message.reply_text(summary)

    except ValueError:
        await update.message.reply_text("Tham số phải là số nguyên. Ví dụ: /new 2") 