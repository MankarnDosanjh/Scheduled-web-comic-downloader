#! python3

# lunarbaboon_downloader.py
# Downloads all comics from https://www.lunarbaboon.com using multithreading.
# NOTE: FINAL_PAGE variable needs to be manually increased to download newer comics.

# Directory change to script location.
import os, sys
os.chdir(os.path.dirname(sys.argv[0]))

# Initilisation of parameters for function call.
FIRST_PAGE = 1
FINAL_PAGE = 200

# Rounds up thread count. Floored division rounds up negative numbers.
THREADS = (-(-FINAL_PAGE // 16))

# Downloads comics from https://www.lunarbaboon.com.
import requests, bs4, time
def lunarbaboon(start_page, end_page):

    HOST = 'http://www.lunarbaboon.com/comics/?currentPage='
    CSS = ['div:nth-child(3) > div:nth-child(3) > p:nth-child(1) > span:nth-child(1) > span:nth-child(1) > img']
    # Creates directory to store comics.
    os.makedirs('./lunarbaboon', exist_ok=True)

    for url_number in range(start_page, end_page):
        
        # Downloads page
        page = f'{HOST}{url_number}'
        res = requests.get(page, verify=False)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        time.sleep(5)
        
        # Searches for image source using CSS selectors.
        css_flag = False
        for selector in CSS:
            comic_elems = soup.select(selector)
            if comic_elems == []: 
                continue

            else:
                css_flag = True
                for elem in comic_elems:
                    # Extracts image source link from CSS selection.
                    comic_url = elem.get('src')

                    if not comic_url.startswith('http'):
                        comic_url = f'http://www.lunarbaboon.com{comic_url}'

                    # Save image to folder.
                    res = requests.get(comic_url, verify=False)
                    res.raise_for_status()
                    time.sleep(5)

                    with open(f'./lunarbaboon/image_{url_number}.jpg', 'wb') as fhandle:
                        for chunk in res.iter_content(100000):
                            fhandle.write(chunk)

# Runs lunarbaboon function with multithreading.
import time, threading
def threaded_execution(start, stop, step, function):
    
    # Starts timer for threaded execution.
    start_time = time.time()
    
    # List used to tie up multiple threads.
    download_threads = []

    # Creates threads.
    for i in range(start, stop, step):
        # Creates unique parameter range for each thread.
        first = i
        last = i + step

        # Initiates threads.
        download_thread = threading.Thread(target=function, args=(first, last))
        download_threads.append(download_thread)
        download_thread.start()

    # Ties up all threads.
    for download_thread in download_threads:
        download_thread.join()

    print(f'\n{function.__name__} comic download finished. Took {time.time() - start_time: .2f} seconds')

lunarbaboon(FIRST_PAGE, FINAL_PAGE)