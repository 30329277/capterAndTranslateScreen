from PIL import ImageGrab
import easyocr
import re
import time

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

# 检查文本是否已经存在于文件中
def is_text_in_file(text, filename='japanese_text.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == text:
                    return True
    except FileNotFoundError:
        pass  # 文件不存在，直接返回 False
    return False

# 保存文本
def save_text(text, filename='japanese_text.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

# 主程序
if __name__ == "__main__":
    while True:
        try:
            # 截图
            image_path = capture_screenshot()
            
            # 识别文本
            japanese_text = recognize_text(image_path)
            
            # 检查识别到的文本是否为空
            if not japanese_text.strip():
                print("No text recognized. Continuing...")
            else:
                # 清理识别到的文本
                cleaned_japanese_text = clean_text(japanese_text)
                
                # 检查文本是否已经存在于文件中
                if is_text_in_file(cleaned_japanese_text):
                    print("Text already exists in the file. Skipping...")
                else:
                    # 保存文本
                    save_text(cleaned_japanese_text)
                    print("Text has been saved.")
            
            # 等待一段时间后继续下一次抓取
            time.sleep(5)  # 你可以根据需要调整等待时间
        except KeyboardInterrupt:
            print("Program interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue