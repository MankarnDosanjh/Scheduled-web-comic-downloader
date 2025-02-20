#! python3

# exocomics_downloader.py
# Downloads all comics from http://www.exocomics.com/ using multithreading.
# NOTE: FINAL_COMIC variable needs to be manually increased to download newer comics.

# Directory change to script location.
import os, sys
os.chdir(os.path.dirname(sys.argv[0]))

# Initialisation of parameters for function call.
FIRST_COMIC = 1
FINAL_COMIC = 764

# Rounds up thread count. Floored division rounds up for negative numbers.
THREADS = (-(-FINAL_COMIC // 16))

# Stores indexes of interactive exocomics comics that can't be parsed with CSS
SPECIAL_COMICS = [200, 300, 400, 500]

# Downloads comics from http://www.exocomics.com/.
import requests, bs4
def exocomics(start_comic, end_comic):
    
    HOST = 'http://www.exocomics.com'
    CSS = '.image-style-main-comic'
    
    # Creates directory to store comics.
    os.makedirs('./exocomics', exist_ok=True)
    
    for url_number in range(start_comic, end_comic):
        # Sub 10 indexes need to be 2 characters to access exocomics page.
        if url_number < 10:
            url_number = '0' + str(url_number)
        
        page = f'{HOST}/{url_number}'
        
        # Exceptions for exocomics special comics which, starting from comic 200, happen every 100 comics.
        if url_number in SPECIAL_COMICS:
            with open('./exocomics_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - {page} is a special interactive comic. Open the link to view it.\n\n')
            continue

        # Downloads page.
        print(f'Downloading page: {page}...')
        try:
            res = requests.get(page)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
        
        except:
            # Writes page download errors to file.
            with open('./exocomics_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - {page} DOWNLOAD FAILED\n\n')
            continue

        # Searches for image source using CSS selector.
        comic_elem = soup.select(CSS)
        
        if comic_elem == []:
            # Writes CSS selection errors to file.     
            with open('./exocomics_errors.txt', 'a') as fhandle:
                fhandle.write(f'ERROR - CSS SELECTOR {CSS} RETURNED NOTHING ON {page}\n\n')
        
        else:
            # Appends image source to host for full image link.
            comic_url = comic_elem[0].get('src')
            comic_url = HOST + comic_url
            
            # Downloads the image.
            print(f'Downloading image {comic_url}...')

            try:
                # Save image to folder.
                res = requests.get(comic_url)
                res.raise_for_status()
                with open(f'./exocomics/{os.path.basename(comic_url)}', 'wb') as fhandle:
                    for chunk in res.iter_content(100000):
                        fhandle.write(chunk)
            
            except:
                # Writes image download errors to file.
                with open('exocomics_errors.txt', 'a') as fhandle:
                    fhandle.write(f'ERROR - {comic_url} DOWNLOAD FAILED\n\n')

# Runs exocomics function with multithreading.
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

threaded_execution(FIRST_COMIC, FINAL_COMIC, THREADS, exocomics)