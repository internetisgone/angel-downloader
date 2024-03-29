```
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     ＼ 。 ☆ 
。 ☆。    ☆  。   ☆。

```
simple command line tool for downloading xiaohongshu images and videos in the highest quality possible. written in python.<br>

inspired by [lux](https://github.com/iawia002/lux) and [xhs-downloader](https://github.com/JoeanAmier/XHS-Downloader). neither fully meets my needs so i wrote angel downloader :D<br>

## setup and run
either execute via the shell script `angel`
```
chmod +x angel
./angel url [options]
```
or run `main.py` directly
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 main.py url [options]
```
<br>

it is recommended that you use a proxy.<br>
change `PROXIES` in `main.py` to something like
```
PROXIES = { "https": "127.0.0.1:1087" }
```

## usage
basic usage:
```
# download all images or video in a post
./angel https://link.to.xhs.post
```
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

## todo
- save metadata
- use a config file
- package the whole thing
