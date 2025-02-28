# Core functionality across two programs
# 1. Downloads comic page urls.
# Parameters: HOST


def download_comic(site: str, css: list[str], range: list[int]):
    # Module imports
    from bs4 import BeautifulSoup
    from urllib.parse import urlparse
    from sys import argv
    import requests
    import os

    res = requests.get(site)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    for selector in css:
        comic_elems = soup.select(selector)
        for elem in comic_elems:
            comic_url = elem.get("src")
            host = urlparse(site).netloc
            if comic_url.startswith("/"):
                comic_url = "/".join(["http:/", host, comic_url])

        res = requests.get(comic_url)
        res.raise_for_status()
        os.chdir(os.path.dirname(argv[0]))
        img_dir = host.split(".")[1]
        img_name = os.path.basename(comic_url)
        os.makedirs(f"./{img_dir}", exist_ok=True)

        with open(f"./{img_dir}/{img_name}", "wb") as fhandle:
            for chunk in res.iter_content(100000):
                fhandle.write(chunk)


comics = {
    "https://www.exocomics.com/":
    [
        [".image-style-main-comic"],
        [1, 764]
    ],

    "https://www.savagechickens.com/category/cartoons/page":
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

for item in comics.items():
    print(item)
