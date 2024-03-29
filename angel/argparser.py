import argparse

parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter,
    prog = "./angel",
    description =
r"""
。 ☆ 。   ☆。     ☆  。
 ☆。\     |     ／。 ☆
   angel downloader
☆。 /     |     \ 。 ☆ 
。 ☆。    ☆  。   ☆。

download high quality xiaohongshu images and videos
""",
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
    help = "indices of images to download. supports negative indices. if no indices are given, all images will be downloaded."
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