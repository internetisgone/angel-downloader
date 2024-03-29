```
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     ＼ 。 ☆ 
。 ☆。    ☆  。   ☆。

```
simple command line tool for downloading xiaohongshu images and videos in the highest quality possible. <br>

inspired by [lux](https://github.com/iawia002/lux) and [xhs-downloader](https://github.com/JoeanAmier/XHS-Downloader). neither fully meets my needs so i wrote angel downloader :D<br>

## install and run
install from wheel
```
pip install dist/angel-0.1.0-py3-none-any.whl
```
or build from source
```
pip install build
python3 -m build
```

then either execute via the shell script `a`
```
chmod +x a
./a [url] [options]
```
or as a package
```
python3 -m angel [url] [options]
```
<br>

## usage
basic usage:
```
# download all images or video in a post
./a https://link.to.xhs.post
```
options:<br>
`-i` to specify image indices
```
# download the 1st, 2nd, and last image
./a https://link.to.xhs.post -i 1 2 -1
```
`-s` to sanitize the url without downloading anything
```
# get full url to the post, removing tracking components
./a https://link.to.xhs.post -s
```
`-h` to show help
```
./a -h  
```
## todo
- save metadata
- use a config file
