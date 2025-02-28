# Core functionality across two programs
# 1. Downloads comic page urls.
# Parameters: HOST

comics = {
    "https://www.exocomics.com/":
    [
        [".image-style-main-comic"],
        [1, 764]
    ],

    "https://www.savagechickens.com/category/cartoons/page/":
    [
        ["div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > img",
         "div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1) > img"],
        [1, 1300]
    ],

    "https://www.lefthandedtoons.com/":
    [
        [".comicimage"],
        [1, 1914]
    ]
}

comics = {
    "https://www.lefthandedtoons.com/":
    [
        [".comicimage"],
        [1, 1914]
    ],

    "https://www.savagechickens.com/category/cartoons/page/":
    [
        ["div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > img",
         "div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1) > img"],
        [1, 1300]
    ]
}


def download_comic(site: str, css: list[str], index_range: list[int]):
    # Module imports
    from bs4 import BeautifulSoup
    from urllib.parse import urlparse
    from sys import argv
    import requests
    import os

    start, stop = index_range

    for i in range(start, stop):
        print(f"Downloading page: {site + str(i)}...")
        res = requests.get(site + str(i))
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        for selector in css:
            comic_elems = soup.select(selector)

            if comic_elems == []:
                continue

            for elem in comic_elems:
                comic_url = elem.get("src")
                host = urlparse(site).netloc
                if comic_url.startswith("/"):
                    comic_url = "/".join(["http:/", host, comic_url])

            print(f"Downloading image: {comic_url}...")
            res = requests.get(comic_url)
            res.raise_for_status()

            img_dir = host.split(".")[1]
            img_name = os.path.basename(comic_url)

            os.chdir(os.path.dirname(argv[0]))
            os.makedirs(f"./{img_dir}", exist_ok=True)

            with open(f"./{img_dir}/{img_name}", "wb") as fhandle:
                for chunk in res.iter_content(100000):
                    fhandle.write(chunk)


def comic_thread(comic):
    import threading

    threads = []

    site = comic[0]
    css = comic[1][0]
    index_range = comic[1][1]

    start, stop = index_range[0], index_range[1]
    step = (-(-stop // 16))

    for i in range(start, stop, step):
        index_range = [i, i + step]

        thread = threading.Thread(target=download_comic, args=(
            site,
            css,
            index_range))

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


for item in comics.items():
    comic_thread(item)
