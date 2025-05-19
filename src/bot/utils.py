import cohere
from .config import COHERE_API_KEY, COHERE_MODEL

def split_message(text, max_length=4000):
    """Chia thông báo thành các phần nhỏ hơn max_length ký tự"""
    if not text:
        return []
        
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_part = ""
    lines = text.split('\n')
    
    for line in lines:
        if len(current_part) + len(line) + 1 <= max_length:
            current_part += line + '\n'
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = line + '\n'
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts

async def summarize_text(text):
    """Tóm tắt văn bản sử dụng Cohere"""
    try:
        if not text:
            return "Không có nội dung để tóm tắt."
            
        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            model=COHERE_MODEL,
            message="Tóm tắt nội dung bài báo sau trong 200-300 từ: " + text
        )
        return response.text if response.text else "Không thể tóm tắt văn bản."
    except Exception as e:
        print(f"Lỗi khi tóm tắt văn bản: {str(e)}")
        return f"Không thể tóm tắt văn bản: {str(e)}"

def extract_keywords(text):
    """Trích xuất từ khóa quan trọng từ văn bản"""
    try:
        if not text:
            return []
            
        co = cohere.Client(COHERE_API_KEY)
        response = co.chat(
            model=COHERE_MODEL,
            message=f"Trích xuất 5-7 từ khóa quan trọng nhất từ văn bản sau, trả về dạng list: {text}"
        )
        return response.text if response.text else []
    except Exception as e:
        print(f"Lỗi khi trích xuất từ khóa: {str(e)}")
        return [] 