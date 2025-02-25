#! python3

# savagechickens_downloader.py
# Downloads all comics from https://www.savagechickens.com using multithreading.
# NOTE: FINAL_PAGE variable needs to be manually increased to download newer comics.

# Directory change to script location.
import os, sys
os.chdir(os.path.dirname(sys.argv[0]))

# Initilisation of parameters for function call.
FIRST_PAGE = 1
FINAL_PAGE = 1300

# Rounds up thread count. Floored division rounds up negative numbers.
THREADS = (-(-FINAL_PAGE // 16))

# Downloads comics from https://www.savagechickens.com.
import requests, bs4, pprint
def savagechickens(start_page, end_page):

    HOST = 'https://www.savagechickens.com/category/cartoons/page'
    CSS = ['div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > img',
           'div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > a:nth-child(1) > img']

    # Creates directory to store comics.
    os.makedirs('./savagechickens', exist_ok=True)

    for url_number in range(start_page, end_page):
        # Downloads page
        page = f'{HOST}/{url_number}'
        print(f'Downloading page: {page}')
        try:
            res = requests.get(page)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
        
        except:
            # Writes page download errors to file.
            with open('./savagechickens_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - {page} DOWNLOAD FAILED\n\n')
            continue
        
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

                    # Downloads the image.
                    print(f'Downloading image {comic_url}...')

                    try:
                        # Save image to folder.
                        res = requests.get(comic_url)
                        res.raise_for_status()
                        with open(f'./savagechickens/{os.path.basename(comic_url)}', 'wb') as fhandle:
                            for chunk in res.iter_content(100000):
                                fhandle.write(chunk)
                    
                    except:
                        # Writes image download errors to file.
                        with open('./savagechickens_errors.txt', 'a') as fhandle:
                            fhandle.write(f'ERROR - {comic_url} DOWNLOAD FAILED\n\n')

        # Writes to file when all CSS selectors fail.    
        if not css_flag:
            with open('./savagechickens_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - {CSS} RETURNED NOTHING ON {page}')

# Runs savagechickens function with multithreading.
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

threaded_execution(FIRST_PAGE, FINAL_PAGE, THREADS, savagechickens)