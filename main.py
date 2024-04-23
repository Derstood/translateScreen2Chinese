from PIL import Image
import pytesseract
from googletrans import Translator
import os
from googletrans import Translator
from difflib import SequenceMatcher
from langdetect import detect_langs

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'


def is_english_within_3_lines(text):
    # 平均词长小于4
    if len(text.split()) * 4 > len(text):
        print("len:", len(text.split()), len(text))
        return False
    print(text, "count:", text.count('\n'))
    if text == "" or text.count('\n') > 2:
        return False
    try:
        results = detect_langs(text)
    except Exception as e:
        print("Error occurred during language detection:", e)
        return False
    for res in results:
        print("lang:", res.lang, "\t prob: ", res.prob)
    if results and (results[0].lang == "en" or results[0].lang == "fr") and results[0].prob > 0.55:
        return True
    return False


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


# 打开图片
screenshot = Image.open("screenshot.png")
# 使用Tesseract进行文字识别
ocr_text = deal_text(pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6'))
if ocr_text != "":
    # 检查与上次OCR文本的相似度
    similarity = SequenceMatcher(None, ocr_text, latest_ocr_text).ratio()
    print("similarity: ", similarity)
    if similarity < 0.8:
        # 翻译识别出的文字
        translator = Translator()
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
