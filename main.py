import time
import random
import requests
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import json
# import mimetypes
import argparse

PROXIES = {
   "http": "127.0.0.1:1087",
   "https": "127.0.0.1:1087",
}
TIMEOUT = 5
SLEEP_INTERVAL_MIN = 2
SLEEP_INTERVAL_MAX = 5

BASE_URL_IMG = "https://ci.xiaohongshu.com/"
IMG_QUERY_STR = "?imageView2/2/w/format/png"
IMG_EXT = ".png"

BASE_URL_VID = "https://sns-video-bd.xhscdn.com/"
VID_EXT = ".mp4"
CHUNK_SIZE = 777777

DOWNLOAD_PATH = "downloads"

def main():
    # create a downloads dir if doesn't exist
    Path(DOWNLOAD_PATH).mkdir(exist_ok = True) 

    # todo check url w regex
    url = sys.argv[1]
    url = url.split("?", 1)[0] # remove tracking 
    if "xhslink" in url:
        url = sanitize_url(url)
    get_page_content(url)

    # todo
    # parser = argparse.ArgumentParser(
    #     prog = "angel downloader",
    #     description = "download xiaohongshu images and videos in the highest quality possible",
    # )
    # parser.add_argument("link")

    # # indices of pics to download
    # # defaults to 0 (all)
    # # supports negative indices (-1 is the last pic)
    # parser.add_argument("-n", "-number", default = 0) 
    # # parser.add_argument("-c", "-clean")
    # # parser.add_argument("-p", "-proxy", action = "store_true")

def sanitize_url(ugly_url):
    response = requests.get(ugly_url, allow_redirects = False)
    url = response.headers["Location"]
    url = url.split("?", 1)[0] 
    return url

def get_page_content(url):
    print(f"getting {url} pls be patient...")
    try: 
        response = requests.get(url, proxies = PROXIES, timeout = TIMEOUT)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # get img
            img_elements = soup.find_all("meta", attrs={"name": "og:image", "content": True})
            if img_elements:
                print(f"found {len(img_elements)} image(s)")
                img_tokens = [meta["content"].split("/")[-1].split("!")[0] for meta in img_elements]
                # todo fall back to meta["content"]
                print(img_tokens)
                get_images(img_tokens)

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
        else:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
        return
    except Exception as e:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")
        return
    
def get_images(tokens):
    for token in tokens:
        try:
            url = BASE_URL_IMG + token + IMG_QUERY_STR
            response = requests.get(url, proxies = PROXIES, timeout = TIMEOUT, stream = True)
            if response.status_code == 200:
                name = token + IMG_EXT
                with open(DOWNLOAD_PATH + "/" + name, "wb") as f:
                    for chunk in response.iter_content(chunk_size = CHUNK_SIZE):
                        f.write(chunk)
                print(f"downloaded image {name}")
            else:
                print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}") 

            interval = random.randint(SLEEP_INTERVAL_MIN, SLEEP_INTERVAL_MAX) 
            print(f"sleeping for {interval} seconds...")
            time.sleep(interval)
        except requests.exceptions.RequestException as e:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
        except Exception as e:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")

def get_video(url):
    try:
        response = requests.get(url, proxies = PROXIES, timeout = TIMEOUT, stream = True)
        if response.status_code == 200:
            name = url.split('/')[-1] + VID_EXT
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