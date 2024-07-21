import time
import random
import httpx
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json
from angel.argparser import parser

URL_PATTERN = re.compile(r"xiaohongshu\.com/((explore)|(discovery/item))/[a-z0-9]+")
URL_PATTERN_SHORT = re.compile(r"xhslink\.com/[A-Za-z0-9]+")

DOWNLOAD_PATH = "Downloads"

BASE_URL_IMG = "https://ci.xiaohongshu.com/"
IMG_QUERY_STR = "?imageView2/2/w/format/png"
IMG_EXT = ".png"

BASE_URL_VID = "https://sns-video-bd.xhscdn.com/"
VID_EXT = ".mp4"

class AngelDownloader:
    def __init__(self, config):
        self.client = httpx.AsyncClient(
            proxy = config["proxy"],
            headers = config["request_headers"],
            timeout = config["timeout"],
            follow_redirects = False,
            max_redirects = 0
            # chunk_size = config["chunk_size"]
        )
    
    async def validate_url(self, url):
        if u := URL_PATTERN.search(url):
            return "https://www." + u.group()
        elif u := URL_PATTERN_SHORT.search(url):
            return await self.sanitize_url("https://" + u.group())
        else:
            return None
    
    # get clean redirected url from a short url
    async def sanitize_url(self, ugly_url) -> str:    
        response = await self.client.get(ugly_url)
        url = response.headers["Location"]
        url = url.split("?", 1)[0] # remove tracking components 
        return url 

    async def get_page_content(self, url, img_indices):
        print(f"getting {url} pls be patient...")
        try: 
            response = await self.client.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # get vid 
                vid_elements = soup.find_all("meta", attrs={"name": "og:video", "content": True})
                if vid_elements:
                    print(f"found {len(vid_elements)} video(s)")

                    # try parse json and get watermark-free vid
                    result = None
                    scripts = soup.find_all("script", src = False, string = True)
                    try: 
                        data_raw = None
                        for script in scripts:
                            if "window.__INITIAL_STATE__=" in script.string:
                                data_raw = script.string.encode().decode("utf-8")
                        if data_raw:
                            data_raw = data_raw.split("window.__INITIAL_STATE__=", 1)[1].replace("undefined", '""')
                            data = json.loads(data_raw)
                            # print("----------------------------------")
                            # print(repr(data))
                            # print("----------------------------------")
                            note_id = data["note"]["firstNoteId"]
                            vid_key = data["note"]["noteDetailMap"][note_id]["note"]["video"]["consumer"]["originVideoKey"]
                            print(vid_key)
                            result = await self.get_video(BASE_URL_VID + vid_key)
                        else:
                            print(f"json not found")
                    except Exception as e:
                        print(e)

                    if not result:
                        # fall back to watermarked ver
                        vid_url = vid_elements[0]["content"]
                        print(f"falling back to watermarked video {vid_url}")
                        await self.get_video(vid_url)
    
                # get img
                else:       
                    img_elements = soup.find_all("meta", attrs={"name": "og:image", "content": True})
                    if img_elements:
                        img_num = len(img_elements)
                        print(f"found {img_num} image(s)")
                        img_tokens = [meta["content"].split("/")[-1].split("!")[0] for meta in img_elements]
                        print(img_tokens)
                        # check if the indices provided are valid 
                        img_indices = validate_img_indices(img_num, img_indices)
                        print(img_indices)
                        if len(img_indices) > 0:
                            img_tokens = [img_tokens[i] for i in img_indices]
                        print(f"fetching images")
                        print(img_tokens)
                        await self.get_images(img_tokens)

            else:
                print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}")
            # except requests.exceptions.RequestException as e:
            #     print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
            #     return
        except Exception as e:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")
            return
        
    async def get_images(self, tokens):
        for index, token in enumerate(tokens):
            try:
                url = BASE_URL_IMG + token + IMG_QUERY_STR
                async with self.client.stream("GET", url) as response:
                    if response.status_code == 200:
                        name = token + IMG_EXT
                        with open(DOWNLOAD_PATH + "/" + name, "wb") as f:
                            async for chunk in response.aiter_bytes():
                                f.write(chunk)
                        print(f"downloaded image {name}")
                    else:
                        print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}") 

                # sleep for some time b4 fetching the next img
                if index < len(tokens) - 1:
                    interval = random.randint(2, 5) / 10 
                    print(f"sleeping for {interval} seconds...")
                    time.sleep(interval)
            # except requests.exceptions.RequestException as e:
            #     print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
            except Exception as e:
                print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")

    async def get_video(self, url) -> bool:
        try:
            async with self.client.stream("GET", url) as response:
                if response.status_code == 200:
                    name = url.split('/')[-1].split("?", 1)[0] + VID_EXT
                    with open(DOWNLOAD_PATH + "/" + name, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                    print(f"downloaded video {name}")
                    return True
                else:
                    print(f"｡ﾟ･ (>_<) ･ﾟ｡ failed to fetch {url}. status code {response.status_code}")
        # except requests.exceptions.RequestException as e:
        #     print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with this request {url} : {e}")
        #     return False
        except Exception as e:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went with {url} : {e}")
            return False
    
    async def close(self):
        await self.client.aclose()

async def main():
    
    # load config from file
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    # create downloader instance
    angelDownloader = AngelDownloader(config)

    args = parser.parse_args()

    url = await angelDownloader.validate_url(args.url)
    if not url:
        print(f"｡ﾟ･ (>_<) ･ﾟ｡ invalid url: {args.url}")
        return

    if args.sanitize == True:
        print(url)
    else:
        # create a downloads dir if doesn't exist
        Path(DOWNLOAD_PATH).mkdir(exist_ok = True) 
        # fetch page
        await angelDownloader.get_page_content(url, args.indices)
   
    await angelDownloader.close()

def validate_img_indices(num, indices) -> list:
    indices = [i - 1 if i > 0 else i for i in indices]
    for i in indices:
        if i > num or i < -num:
            indices.remove(i)
    return indices

if __name__ == "__main__":
    asyncio.run(main())