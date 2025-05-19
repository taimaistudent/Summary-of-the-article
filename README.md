# News Analysis Telegram Bot

Bot Telegram tự động tóm tắt và phân tích tin tức từ các trang web tiếng Việt.

## Tính năng

- Tóm tắt tin tức từ các nguồn:
  - VnExpress
  - Cafef
  - DevOps.vn
- Hỗ trợ 3 cách sử dụng cho mỗi nguồn:
  - Lấy bài viết đầu tiên
  - Lấy bài viết theo số thứ tự
  - Phân tích bài viết từ link cụ thể

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/your-username/news-analysis-bot.git
cd news-analysis-bot
```

2. Tạo môi trường ảo và cài đặt dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Tạo file .env từ .env.example và cập nhật các biến môi trường:
```bash
cp .env.example .env
```

4. Chạy bot:
```bash
python src/main.py
```

## Sử dụng Docker

1. Build image:
```bash
docker build -t news-analysis-bot .
```

2. Chạy container:
```bash
docker run -d --name news-bot news-analysis-bot
```

## Các lệnh của bot

- `/start` - Lấy bài viết đầu tiên từ VnExpress
- `/new <n>` - Lấy bài viết thứ n từ VnExpress
- `/link <url> [n]` - Phân tích bài viết từ URL
- `/devops [n|url]` - Lấy bài viết từ DevOps.vn
- `/cafef [n|url]` - Lấy bài viết từ Cafef
- `/vnexpress [n|url]` - Lấy bài viết từ VnExpress

## Cấu trúc dự án

```
news-analysis-bot/
├── src/
│   ├── main.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── utils.py
│   └── scrapers/
│       ├── __init__.py
│       └── news_scrapers.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request.

## License

MIT 