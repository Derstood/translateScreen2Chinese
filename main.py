from PIL import ImageGrab
import pytesseract
from googletrans import Translator
import keyboard
import os
import tkinter as tk
import threading
import time
from difflib import SequenceMatcher
from langdetect import detect_langs


def is_english_within_3_lines(text):
    if text == "" or text.count('\n') > 2:
        return False
    try:
        results = detect_langs(text)
    except Exception as e:
        print("Error occurred during language detection:", e)
        return False
    if results and results[0].lang == "en" and results[0].prob > 0.8:
        return True
    return False


os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'
translator = Translator()

# 全局变量，用于存储最新的OCR文本和翻译后文本
latest_ocr_text = ""
latest_translated_text = ""
translate_times = 0


# 处理文本函数
def deal_text(text):
    if is_english_within_3_lines(text):
        return text.replace('<<', '')\
            .replace('_', '') \
            .replace('|', 'I') \
            .replace('\n', ' ') \
            .replace('@', '') \
            .replace('=', '') \
            .replace('“', '') \
            .replace('”', '') \
            .replace('-', '') \
            .replace('NICK', '尼克')
    return ""


# 截图、OCR、翻译循环线程函数
def capture_translate_thread():
    global latest_ocr_text, latest_translated_text, translate_times
    while True:
        # 截图
        screenshot = ImageGrab.grab(bbox=(650, 1140, 1900, 1380)).convert('L').point(lambda p: p > 150 and 255)
        screenshot.save("screenshot.png")
        # 使用Tesseract进行文字识别
        ocr_text = deal_text(pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6'))
        if ocr_text != "":
            # 检查与上次OCR文本的相似度
            similarity = SequenceMatcher(None, ocr_text, latest_ocr_text).ratio()
            print("similarity: ", similarity)
            if similarity < 0.8:
                # 翻译识别出的文字
                translated = translator.translate(ocr_text, src='en', dest='zh-cn')
                if translated.text:
                    translated_text = translated.text
                else:
                    translated_text = "TRANSLATE ERROR"
                translate_times += 1
                print("ori text:", ocr_text)
                print("translated text:", translated_text)
                if translated_text != "":
                    # 更新最新的OCR文本和翻译后文本
                    latest_ocr_text = ocr_text
                    latest_translated_text = translated_text
        # 等待2秒后继续循环
        time.sleep(1)


# 监听F12按键并弹窗线程函数
def f12_listener_thread():
    global latest_translated_text
    while True:
        keyboard.wait('f12')
        # 创建弹窗并显示最新的翻译后文本
        if latest_translated_text == "":
            latest_translated_text = "NULL"
        root = tk.Tk()
        root.title(str(translate_times))
        text_label = tk.Label(root, text=latest_translated_text, wraplength=880, justify="left", font=("Arial", 25))
        text_label.pack(padx=10, pady=10)
        # 等待更新窗口布局
        root.update_idletasks()
        # 根据文本内容的高度调整窗口大小
        text_height = text_label.winfo_reqheight()
        # 将窗口置顶
        root.attributes("-topmost", True)
        root.geometry(f"920x{text_height + 20}+400+500")
        # 等待3秒后关闭窗口
        root.after(2000, root.destroy)
        root.mainloop()


# 启动截图、OCR、翻译循环线程
capture_translate_thread = threading.Thread(target=capture_translate_thread)
capture_translate_thread.daemon = True
capture_translate_thread.start()

# 启动监听F12按键弹窗线程
f12_listener_thread = threading.Thread(target=f12_listener_thread)
f12_listener_thread.daemon = True
f12_listener_thread.start()

# 进入主线程等待状态，直到按下ESC键退出程序
keyboard.wait('esc')
