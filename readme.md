```
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     ＼ 。 ☆ 
。 ☆。    ☆  。   ☆。

```
simple command line tool for downloading xiaohongshu images and videos in the highest quality possible. <br>

inspired by [lux](https://github.com/iawia002/lux) and [xhs-downloader](https://github.com/JoeanAmier/XHS-Downloader). neither fully meets my needs so i wrote angel downloader :D<br>

## setup
either install from wheel
```
pip install angel-0.2.0-py3-none-any.whl
```
or build from source
```
pip install build
python3 -m build
```
edit `config.json` accordingly
## run
as a package
```
python3 -m angel [url] [options]
```
or via the shell script `a`
```
chmod +x a
./a [url] [options]
```

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
./a -i 1 2 -1 https://xhslink.com/gnome 
```
`-s` to sanitize a short url without downloading anything
```
# get full url to the post, removing tracking components
./a -s https://xhslink.com/gnome
```
`-h` to show help
```
./a -h  
```
## todo
- save metadata
- ~~use a config file~~

## misc
for simply sanitizing links, [this shell script](https://gist.github.com/internetisgone/22e296dbb541eb6e73486568230bd9ff) and [this resolver](https://github.com/usexhs/xhs-link) can also come in handy