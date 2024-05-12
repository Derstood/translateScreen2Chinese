# translateScreen2Chinese
translateScreen to Chinese
### usage:
| 按键 | 功能   |
|---|---|
| F12 | show |
| F11 | hide |
| Ctrl +ESC | exit|

首次运行会在当前路径下载模型到model目录

### TODO list
1. 指定框选屏幕位置(现在是下方字幕，方便自己实际使用)
2. 多个框选位置寄存，快速来回切换框选
3. 加个程序图标
4. UI优化（预计v0.8开始做）

### Note：
google translator无需本地模型，在[google_trans分支](https://github.com/Derstood/translateScreen2Chinese/tree/google_trans)大陆地区无法使用，<br>
需要配合10808 10809<br><br>
如果已经肉身在外，可以删掉这几行：
```python3
import os
...
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'
```

### env:
pip install transformers sentencepiece torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple

### 生成exe:
pyinstall ./main.spec


# change log
## 0.2
### 2024-05-13
使用本地模型，翻译响应速度从googletrans的2秒提升到python本地translator的4秒后，又降至0.1s
## 0.1
### 2024-04-21
Basaic function
