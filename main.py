from PIL import ImageGrab
import pytesseract
from googletrans import Translator
import keyboard
import os
import tkinter as tk
import threading
import time
from difflib import SequenceMatcher
from skimage.metrics import structural_similarity as ssim
import numpy as np
from datetime import datetime
from transformers import MarianMTModel, MarianTokenizer


def is_conversation_within_3_lines(text):
    # 平均单词的长度大于3
    if len(text.split()) * 3 > len(text):
        return False
    # 不为空且最多3行
    if text == "" or text.count('\n') > 3:
        return False
    return True


os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

# 加载预训练模型和分词器
cache_dir = "./model/"
model_name = "Helsinki-NLP/opus-mt-en-zh"
tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = MarianMTModel.from_pretrained(model_name, cache_dir=cache_dir)

print("Init Finished")

translator = Translator()

# 全局变量，用于存储最新的OCR文本和翻译后文本
latest_ocr_text = ""
latest_translated_text = ""
latest_screenshot = None
previous_screenshot = None
translate_times = 0

# 创建窗口并设置隐藏状态
root = tk.Tk()
root.withdraw()

# 创建用于显示翻译后文本的 Label
translated_text_label = tk.Label(root, text="", wraplength=880, justify="left", font=("Arial", 25))
translated_text_label.pack(padx=10, pady=10)

replacements = {
    '<<': '',
    '_': '',
    '|': 'I',
    '\n': ' ',
    '@': '',
    '=': '',
    '“': '',
    '”': '',
    '-': '',
    'NICK': '尼克',
}


# 处理文本函数
def deal_text(text):
    if is_conversation_within_3_lines(text):
        global replacements
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    return ""


# 截图、OCR、翻译循环线程函数
def capture_translate_thread():
    global latest_ocr_text, latest_translated_text, latest_screenshot, previous_screenshot, translate_times
    while True:
        # 截图
        screenshot = ImageGrab.grab(bbox=(650, 1140, 1900, 1380)).convert('L').point(lambda p: p > 180 and 255)
        screenshot_array = np.array(screenshot)
        # 如果图片全黑或全白
        if np.all(screenshot_array == 0) or np.all(screenshot_array == 255):
            time.sleep(0.3)
            continue
        if previous_screenshot:
            # 如果相似度高，则跳过 OCR 和翻译
            similarity = ssim(np.array(previous_screenshot), screenshot_array)
            if similarity > 0.95:
                time.sleep(0.3)
                continue
        screenshot.save("latest_screenshot.png")
        # 使用Tesseract进行文字识别
        ocr_text = deal_text(pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6'))
        if ocr_text != "":
            # 翻译识别出的文字
            print(f"begin: {datetime.now().time()}")
            translated_ids = model.generate(tokenizer(ocr_text, return_tensors="pt")["input_ids"])
            translated = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
            # translated = translator.translate(ocr_text, src='en', dest='zh-cn')
            print(f"after: {datetime.now().time()}")
            if translated:
                translated_text = translated
            else:
                translated_text = "TRANSLATE ERROR"
            translate_times += 1
            print("ori text:", ocr_text)
            print("translated text:", translated_text)
            if translated_text != "":
                # 更新最新的OCR文本和翻译后文本
                latest_ocr_text = ocr_text
                latest_translated_text = translated_text
                # 将翻译后的文本同步到窗口中
                translated_text_label.config(text=latest_translated_text)
                # 更新窗口高度
                text_height = translated_text_label.winfo_reqheight()
                root.geometry(f"920x{text_height + 20}+400+550")
                # 更新标题
                root.title(f"Translate Times: {translate_times}")
                previous_screenshot = screenshot
                previous_screenshot.save("previous_screenshot.png")
        # 等待0.3秒后继续循环
        time.sleep(0.3)


# 监听F12按键并显示翻译后文本的窗口函数
def show_translated_text_window():
    global root
    root.deiconify()
    # 确保窗口始终在顶层
    root.attributes("-topmost", True)


def hide_translated_text_window():
    global root
    root.withdraw()


def exit_app():
    global root, translated_text_label
    # 将翻译后的文本同步到窗口中
    text = "退出使用"
    translated_text_label.config(text=text)
    text_height = translated_text_label.winfo_reqheight()
    root.geometry(f"920x{text_height + 20}+400+500")
    show_translated_text_window()
    time.sleep(2)
    root.quit()


# 启动截图、OCR、翻译循环线程
capture_translate_thread = threading.Thread(target=capture_translate_thread)
capture_translate_thread.daemon = True
capture_translate_thread.start()

# 监听F12按键并显示翻译后文本的窗口
keyboard.add_hotkey('f12', show_translated_text_window)
keyboard.add_hotkey('f11', hide_translated_text_window)

# 启动监听ESC按键并退出程序
keyboard.add_hotkey('ctrl+esc', exit_app)

# 主线程进入事件循环
root.mainloop()
