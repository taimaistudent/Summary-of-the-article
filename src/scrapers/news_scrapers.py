import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

async def get_html_links_from_url(url):
    """Lấy danh sách link bài viết từ URL cho vnexpress, cafef, devops.vn"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        html_links = []
        # Các từ khóa nhận diện link bài viết
        keywords = ['bai-viet', 'news', 'article', 'post', 'tin', 'story', '.html', '.chn', '/events/']
        for item in soup.find_all('a', href=True):
            link = item['href']
            # Lấy link nội bộ hoặc link ngoài, có chứa từ khóa bài viết
            if (
                (link.startswith('/') or link.startswith('http')) and
                any(kw in link for kw in keywords)
            ):
                # Chuẩn hóa link nếu là link nội bộ
                if link.startswith('/'):
                    link = urljoin(url, link)
                html_links.append(link)
        # Loại bỏ trùng lặp, giữ thứ tự
        return list(dict.fromkeys(html_links))
    except Exception as e:
        print(f'Lỗi khi lấy links từ {url}: {str(e)}')
        return []

async def get_devops_content(url):
    """Lấy nội dung bài viết từ devops.vn"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm nội dung bài viết
        content = None
        
        # Thử tìm theo các class phổ biến
        for class_name in ['tdb-block-inner', 'tdb_single_content', 'tdb-block-inner td-fix-index']:
            content_div = soup.find('div', class_=class_name)
            if content_div:
                content = content_div
                break
                
        # Nếu không tìm thấy, thử tìm theo thẻ article
        if not content:
            article = soup.find('article')
            if article:
                # Loại bỏ các phần không cần thiết
                for div in article.find_all(['div', 'script', 'style']):
                    div.decompose()
                content = article
                
        # Nếu vẫn không tìm thấy, thử lấy toàn bộ nội dung chính
        if not content:
            main_content = soup.find('main') or soup.find('div', class_='main-content')
            if main_content:
                # Loại bỏ các phần không cần thiết
                for div in main_content.find_all(['div', 'script', 'style']):
                    div.decompose()
                content = main_content
                
        # Nếu vẫn không tìm thấy, thử lấy nội dung từ body
        if not content:
            body = soup.find('body')
            if body:
                # Loại bỏ các phần không cần thiết
                for div in body.find_all(['div', 'script', 'style', 'header', 'footer', 'nav']):
                    div.decompose()
                content = body
                
        if content:
            # Làm sạch nội dung
            text = content.get_text(separator='\n', strip=True)
            text = re.sub(r'\n{3,}', '\n\n', text)  # Giảm số dòng trống
            text = re.sub(r'\s+', ' ', text)  # Loại bỏ khoảng trắng thừa
            return text.strip()
            
        # Nếu không tìm thấy nội dung, in ra HTML để debug
        print(f"Không tìm thấy nội dung trong HTML của {url}")
        print("HTML:", soup.prettify()[:1000])  # In 1000 ký tự đầu tiên của HTML
        return None
    except Exception as e:
        print(f"Lỗi khi lấy nội dung từ {url}: {str(e)}")
        return None

async def get_cafef_content(url):
    """Lấy nội dung bài viết từ cafef.vn"""
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm nội dung bài viết
        content = None
        
        # Thử tìm theo class phổ biến
        content_div = soup.find('div', class_='detail-content')
        if content_div:
            content = content_div
        else:
            # Thử tìm theo cấu trúc khác
            article = soup.find('article') or soup.find('div', class_='article-content')
            if article:
                # Loại bỏ các phần không cần thiết
                for div in article.find_all(['div', 'script', 'style']):
                    div.decompose()
                content = article
                
        if content:
            # Làm sạch nội dung
            text = content.get_text(separator='\n', strip=True)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
            
        return None
    except Exception as e:
        print(f"Lỗi khi lấy nội dung từ {url}: {str(e)}")
        return None

async def get_vnexpress_content(url):
    """Lấy nội dung bài viết từ vnexpress.net"""
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm nội dung bài viết
        content = None
        
        # Thử tìm theo class phổ biến
        content_div = soup.find('div', class_='detail-content')
        if content_div:
            content = content_div
        else:
            # Thử tìm theo cấu trúc khác
            article = soup.find('article') or soup.find('div', class_='sidebar_1')
            if article:
                # Loại bỏ các phần không cần thiết
                for div in article.find_all(['div', 'script', 'style']):
                    div.decompose()
                content = article
                
        if content:
            # Làm sạch nội dung
            text = content.get_text(separator='\n', strip=True)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
            
        return None
    except Exception as e:
        print(f"Lỗi khi lấy nội dung từ {url}: {str(e)}")
        return None 