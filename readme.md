```
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     ＼ 。 ☆ 
。 ☆。    ☆  。   ☆。

```
simple command line tool for downloading xiaohongshu images and videos in the highest quality possible. written in python.<br>

inspired by https://github.com/iawia002/lux and https://github.com/JoeanAmier/XHS-Downloader.<br>

## setup and run
either execute via the shell script `angel`
```
chmod +x angel
./angel https://link.to.xhs.post [options]
```
or run `main.py` directly
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py https://link.to.xhs.post [options]
```

## usage
basic usage:
```
# download all images or video in a post
./angel https://link.to.xhs.post
```
<br>

options:<br>
`-i` to specify image indices
```
# download the 1st, 2nd, and last image
./angel https://link.to.xhs.post -i 1 2 -1
```
`-s` to sanitize the url without downloading anything
```
# get full url to the post, removing tracking components
./angel https://link.to.xhs.post -s
```
`-h` to show help
```
./angel -h  
```