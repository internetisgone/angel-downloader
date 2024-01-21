```
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     ＼ 。 ☆ 
。 ☆。    ☆  。   ☆。

```
simple python command line tool that downloads xiaohongshu images and videos in the highest quality possible.<br>

inspired by https://github.com/iawia002/lux and https://github.com/JoeanAmier/XHS-Downloader<br>

## setup
either
```
chmod +x angel.sh
./angel.sh https://link.to.xhs.post [options]
```
or
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py https://link.to.xhs.post [options]
```

## usage
basic usage
```
# download all images or video in a post
./angel.sh https://link.to.xhs.post
```

option `-i` to specify image indices
```
# download the 1st, 2nd, and last image
./angel.sh https://link.to.xhs.post -i 1 2 -1
```

option `-s` to sanitize the url without downloading anything
```
# returns full url to the post, removing tracking components
./angel.sh https://link.to.xhs.post -s
```

`-h` to show help

## todo
all kinds of exception handling<br>
add support for negative indices (-1 leads to the last img)