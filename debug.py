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


# 加载预训练模型和分词器
cache_dir = "./model/"
model_name = "Helsinki-NLP/opus-mt-en-zh"
tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True, force_download=False)
model = MarianMTModel.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True, force_download=False)

print("Init Finished")

translator = Translator()


ocr_text = r"Of course! We're just... celebrating. "
print(f"begin: {datetime.now().time()}")
translated_ids = model.generate(tokenizer(ocr_text, return_tensors="pt")["input_ids"],
                                max_length=50,  # 设置最大生成长度
                                do_sample=True,  # 进行采样
                                top_p=0.9,  # 使用top-p采样
                                temperature=0.9,  # 设置温度
                                repetition_penalty=1.2,  # 设置重复惩罚
                                no_repeat_ngram_size=3,)
translated = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
print(f"after: {datetime.now().time()}")
print("ori text:", ocr_text)
print("translated text:", translated)
