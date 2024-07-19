## downloading no longer works cuz of anti-bot measures. archiving the repo for now, might come back to it later. the -s (--sanitize-only) option is not affected 
## im also using [this shell script](https://gist.github.com/internetisgone/22e296dbb541eb6e73486568230bd9ff) to sanitize links

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
./a https://xhslink.com/gnome
```
options:<br>
`-i` to specify image indices
```
# download the 1st, 2nd, and last image
./a https://xhslink.com/gnome -i 1 2 -1
```
`-s` to sanitize a short url without downloading anything
```
# get full url to the post, removing tracking components
./a https://xhslink.com/gnome -s
```
`-h` to show help
```
./a -h  
```
## todo
- save metadata
- use a config file
