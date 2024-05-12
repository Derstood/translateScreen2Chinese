# translateScreen2Chinese
translateScreen to Chinese
### usage:
| 按键 | 功能   |
|---|---|
| F12 | show |
| F11 | hide |
| Ctrl +ESC | exit|

### Note：
google translator大陆地区无法使用，<br>
需要配合10808 10809<br><br>
如果已经肉身在外，可以删掉这两行：
```python3
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'
```

### env:
pip install transformers sentencepiece torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple


# change log
## 0.2
### 2024-05-13
使用本地模型，翻译响应速度从googletrans的2秒提升到python本地translator的4秒后，又降至0.1s
## 0.1
### 2024-04-21
Basaic function
