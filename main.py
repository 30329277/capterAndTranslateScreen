from PIL import ImageGrab
import easyocr
import requests
import hashlib
from urllib.parse import quote
import re

# 抓取屏幕正上方居中位置800x90像素的区域
def capture_screenshot():
    # 假设屏幕分辨率为3440x1440
    screen_width = 3440
    screen_height = 1440
    x_start = (screen_width - 800) // 2
    y_start = 0
    x_end = x_start + 800
    y_end = y_start + 90
    
    screenshot = ImageGrab.grab(bbox=(x_start, y_start, x_end, y_end))
    screenshot.save('screenshot.png')
    return 'screenshot.png'

# 使用 EasyOCR 识别日语文本
def recognize_text(image_path):
    reader = easyocr.Reader(['ja'])  # 只加载日语模型
    result = reader.readtext(image_path, detail=0)  # detail=0表示只返回文字
    recognized_text = ' '.join(result)
    print(f"Recognized Japanese Text: {recognized_text}")
    return recognized_text

# 清理识别到的文本
def clean_text(text):
    # 去除特殊字符和多余空格
    cleaned_text = re.sub(r'[^ぁ-んァ-ン一-龥\s]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    print(f"Cleaned Japanese Text: {cleaned_text}")
    return cleaned_text

# 翻译文本
def translate(text, from_lang='ja', to_lang='zh'):
    if not text.strip():
        print("Empty text, skipping translation.")
        return None

    appid = '20230315001600642'  # 你的百度翻译应用ID
    secret_key = 'CC0cSo8X3M3xBlFsqgI8'  # 你的百度翻译秘钥
    salt = '123456'  # 随机数，可以是任意字符串
    sign = hashlib.md5((appid + text + salt + secret_key).encode()).hexdigest()
    
    url = f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={quote(text)}&from={from_lang}&to={to_lang}&appid={appid}&salt={salt}&sign={sign}'
    print(f"API Request URL: {url}")  # 打印完整的API请求URL用于调试
    
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        print(f"API Response: {result}")  # 打印API响应内容用于调试
        if 'trans_result' in result and len(result['trans_result']) > 0:
            return result['trans_result'][0]['dst']
        else:
            print("Translation failed: 'trans_result' not found in API response")
            return None
    else:
        print(f"Translation failed: {response.status_code}")
        return None

# 保存翻译后的文本
def save_text(text, filename='translated_text.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

# 主程序
if __name__ == "__main__":
    # 截图
    image_path = capture_screenshot()
    
    # 识别文本
    japanese_text = recognize_text(image_path)
    
    # 检查识别到的文本是否为空
    if not japanese_text.strip():
        print("No text recognized. Exiting.")
    else:
        # 清理识别到的文本
        cleaned_japanese_text = clean_text(japanese_text)
        
        # 翻译文本
        chinese_text = translate(cleaned_japanese_text)
        if chinese_text:
            print(f"Translated Chinese Text: {chinese_text}")
            
            # 保存文本
            save_text(chinese_text)
            print("Text has been saved.")
        else:
            print("Translation failed. No text to save.")