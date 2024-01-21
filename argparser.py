import argparse

parser = argparse.ArgumentParser(
    prog = 
r"""
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     \ 。 ☆ 
。 ☆。    ☆  。   ☆。
""", 
    description = "download xiaohongshu images and videos in the highest quality possible",
)

parser.add_argument(
    "url",
    type = str,
    help = "link to the xiaohongshu post you wish to download. supports both xhslink.com and xiaohongshu.com"
)

parser.add_argument(
    "-i", 
    "--indices", 
    dest = "indices",
    default = [], 
    nargs = "+",
    type = int,
    required = False,
    help = "indices of images to download. defaults to 0 which will download all images. supports negative indices."
) 

parser.add_argument(
    "-s", 
    "--sanitize-only", 
    dest = "sanitize",
    default = False,
    required = False,
    action = "store_true",
    help = "get the sanitized url without downloading anything."
)