#! python3

# lefthandedtoons_downloader.py
# Downloads all comics from https://www.lefthandedtoons.com using multithreading.
# NOTE: FINAL_COMIC variable needs to be manually increased to download newer comics.

# Directory change to script location.
import os, sys
os.chdir(os.path.dirname(sys.argv[0]))

# Initialisation of parameters for function call.
FIRST_COMIC = 1
FINAL_COMIC = 1914

# Rounds up thread count. Floored division rounds up for negative numbers.
THREADS = (-(-FINAL_COMIC // 16))

# Downloads comics from https://www.lefthandedtoons.com.
import requests, bs4
def lefthandedtoons(start_comic, end_comic):
    
    HOST = 'https://www.lefthandedtoons.com'
    CSS = '.comicimage'
    
    # Creates directory to store comics.
    os.makedirs('./lefthandedtoons', exist_ok=True)
    
    for url_number in range(start_comic, end_comic):
        # Downloads page.
        page = f'{HOST}/{url_number}'        
        print(f'Downloading page: {page}...')
        try:
            res = requests.get(page)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
        
        except:
            # Writes page download errors to file.
            with open('./lefthandedtoons_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - {page} DOWNLOAD FAILED\n\n')
            continue

        # Searches for image source using CSS selector.
        comic_elem = soup.select(CSS)
        
        if comic_elem == []:
            # Writes CSS selection errors to file.     
            with open('./lefthandedtoons_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - CSS SELECTOR {CSS} RETURNED NOTHING ON {page}\n\n')
        
        else:
            # Extracts image source link from CSS selection.
            comic_url = comic_elem[0].get('src')    
            
            # Downloads the image.
            print(f'Downloading image {comic_url}...')

            try:
                # Save image to folder.
                res = requests.get(comic_url)
                res.raise_for_status()
                with open(f'./lefthandedtoons/{os.path.basename(comic_url)}', 'wb') as fhandle:
                    for chunk in res.iter_content(100000):
                        fhandle.write(chunk)
            
            except:
                # Writes image download errors to file.
                with open('lefthandedtoons_errors.txt', 'a') as fhandle:
                    fhandle.write(f'ERROR - {comic_url} DOWNLOAD FAILED\n\n')

# Runs lefthandedtoons function with multithreading.
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

threaded_execution(FIRST_COMIC, FINAL_COMIC, THREADS, lefthandedtoons)