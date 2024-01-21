import time
import random
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json
from argparser import parser

PROXIES = None
HEADERS = None

# PROXIES = {
#     "https": "127.0.0.1:1087"
# }
# HEADERS = {
#     "user-agent": "angel"
# }

TIMEOUT = 10
SLEEP_INTERVAL_MIN = 2
SLEEP_INTERVAL_MAX = 5

BASE_URL_IMG = "https://ci.xiaohongshu.com/"
IMG_QUERY_STR = "?imageView2/2/w/format/png"
IMG_EXT = ".png"

BASE_URL_VID = "https://sns-video-bd.xhscdn.com/"
VID_EXT = ".mp4"
CHUNK_SIZE = 7777777

DOWNLOAD_PATH = "downloads"

URL_PATTERN = re.compile(r"xiaohongshu\.com/((explore)|(discovery/item))/[a-z0-9]+")
URL_PATTERN_SHORT = re.compile(r"xhslink\.com/[A-Za-z0-9]+")

def main():
    args = parser.parse_args()
    # print(args.url)
    # print(args.indices)
    # print(args.sanitize)

    url = validate_url(args.url)
    if not url:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ invalid url: {args.url}")
        return

    if args.sanitize == True:
        print(url)
    else:
        # create a downloads dir if doesn't exist
        Path(DOWNLOAD_PATH).mkdir(exist_ok = True) 
        # fetch page
        get_page_content(url, args.indices)

def validate_url(url):
    if u := URL_PATTERN.search(url):
        return "https://www." + u.group()
    elif u := URL_PATTERN_SHORT.search(url):
        return sanitize_url("https://" + u.group())
    else:
        return None

def sanitize_url(ugly_url) -> str:
    response = requests.get(
        ugly_url, 
        proxies = PROXIES,
        headers = HEADERS,
        timeout = TIMEOUT,
        allow_redirects = False
    )
    url = response.headers["Location"]
    url = url.split("?", 1)[0] 
    return url

def validate_img_indices(num, indices) -> list:
    indices = [i - 1 if i > 0 else i for i in indices]
    for i in indices:
        if i > num or i < -num:
            indices.remove(i)
    return indices

def get_page_content(url, img_indices):
    print(f"getting {url} pls be patient...")
    try: 
        response = requests.get(
            url, 
            proxies = PROXIES, 
            headers = HEADERS,  
            timeout = TIMEOUT
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # get vid 
            vid_elements = soup.find_all("meta", attrs={"name": "og:video", "content": True})
            if vid_elements:
                print(f"found {len(vid_elements)} video(s)")

                # try parse json and get watermark-free vid
                scripts = soup.find_all("script", src = False, string = True)
                result = None
                try: 
                    data_raw = scripts[-1].string
                    data_raw = data_raw.encode().decode("utf-8")
                    data_raw = data_raw.split("window.__INITIAL_STATE__=", 1)[1].replace("undefined", '""')
                    data = json.loads(data_raw)
                    # print("----------------------------------")
                    # print(repr(data))
                    # print("----------------------------------")
                    note_id = data["note"]["firstNoteId"]
                    vid_key = data["note"]["noteDetailMap"][note_id]["note"]["video"]["consumer"]["originVideoKey"]
                    print(vid_key)
                    result = get_video(BASE_URL_VID + vid_key)
                except Exception as e:
                    print(e)

                if not result:
                    # fall back to watermarked ver
                    vid_url = vid_elements[0]["content"]
                    print(f"falling back to watermarked video {vid_url}")
                    get_video(vid_url)
 
            # get img
            else:       
                img_elements = soup.find_all("meta", attrs={"name": "og:image", "content": True})
                if img_elements:
                    img_num = len(img_elements)
                    print(f"found {img_num} image(s)")
                    img_tokens = [meta["content"].split("/")[-1].split("!")[0] for meta in img_elements]
                    # check if the indices provided are valid 
                    img_indices = validate_img_indices(img_num, img_indices)
                    if len(img_indices) > 0:
                        img_tokens = [img_tokens[i] for i in img_indices]
                    print(f"fetching images")
                    print(img_tokens)
                    get_images(img_tokens)
                    # todo fall back to watermarked ver

        else:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
        return
    except Exception as e:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")
        return
    
def get_images(tokens):
    for index, token in enumerate(tokens):
        try:
            url = BASE_URL_IMG + token + IMG_QUERY_STR
            with requests.get(
                url, 
                proxies = PROXIES, 
                headers = HEADERS, 
                timeout = TIMEOUT, 
                stream = True
            ) as response:
                if response.status_code == 200:
                    name = token + IMG_EXT
                    with open(DOWNLOAD_PATH + "/" + name, "wb") as f:
                        for chunk in response.iter_content(chunk_size = CHUNK_SIZE):
                            f.write(chunk)
                    print(f"downloaded image {name}")
                else:
                    print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}") 
            # sleep for some time b4 fetching the next img
            if index < len(tokens) - 1:
                interval = random.randint(SLEEP_INTERVAL_MIN, SLEEP_INTERVAL_MAX) 
                print(f"sleeping for {interval} seconds...")
                time.sleep(interval)
        except requests.exceptions.RequestException as e:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
        except Exception as e:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")

def get_video(url) -> bool:
    try:
        with requests.get(
            url, 
            proxies = PROXIES, 
            timeout = TIMEOUT, 
            headers = HEADERS, 
            stream = True
        ) as response:
            if response.status_code == 200:
                name = url.split('/')[-1].split("?", 1)[0] + VID_EXT
                with open(DOWNLOAD_PATH + "/" + name, "wb") as f:
                    for chunk in response.iter_content(chunk_size = CHUNK_SIZE):
                        f.write(chunk)
                print(f"downloaded video {name}")
                return True
            else:
                print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
        return False
    except Exception as e:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")
        return False

if __name__ == "__main__":
    main()