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
