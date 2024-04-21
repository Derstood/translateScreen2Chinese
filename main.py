from PIL import ImageGrab
import pytesseract
from googletrans import Translator
import keyboard
import os
import tkinter as tk
from tkinter import messagebox

translator = Translator()

def close_window(root):
    root.destroy()
def on_F12_pressed(event):
    # 截图
    screenshot = ImageGrab.grab(bbox=(650, 1140, 1900,1380))
    screenshot.save("screenshot.png")
    # 使用Tesseract进行文字识别
    text = pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6')\
        .replace('<<', '')\
        .replace('_', '')\
        .replace('|', 'I')\
        .replace('\n', ' ')\
        .replace('@', '') \
        .replace('=', '') \
        .replace('“', '') \
        .replace('”', '') \
        .replace('-', '')
    if text == "":
        return
    # 翻译识别出的文字
    translated_text = translator.translate(text, src='en', dest='zh-cn').text
    print("原文本：", text)
    print("翻译后：", translated_text)
    # 创建弹窗并显示识别出的文字
    if translated_text != "":
        root = tk.Tk()
        text_label = tk.Label(root, text=translated_text, wraplength=880, justify="left", font=("Arial", 25))
        text_label.pack(padx=10, pady=10)
        # 等待更新窗口布局
        root.update_idletasks()
        # 根据文本内容的高度调整窗口大小
        text_height = text_label.winfo_reqheight()
        # 将窗口置顶
        root.attributes("-topmost", True)
        root.geometry(f"920x{text_height + 20}+400+500")
        root.after(3000, close_window, root)
        root.mainloop()


# 绑定键盘事件
keyboard.on_press_key('f12',on_F12_pressed)
# 进入监听状态
keyboard.wait('esc')
