#! python3

'''Scheduled Web Comic Downloader

Write a program that checks the websites of several web comics and
automatically downloads the images if the comic was updated since
the program's last visit. Your operating system's scheduler
(Scheduled Tasks on Windows, launchd on macOS, and cron on Linux)
can run your Python program once a day. The Python program itself
can download the comic and then copy it to your desktop so that it
is easy to find. This will free you from having to check the
website yourself to see whether it has updated. (A list of web
comics is available at:
https://automatetheboringstuff.com/list-of-web-comics.html)'''

import inspect, os, sys, time, requests, bs4, threading, traceback
os.chdir(os.path.dirname(sys.argv[0]))

# General process
# TODO: Create directory to store webcomic
# TODO: Create URLs using an iterating variable
# TODO: Download site's HTML and parse with BS4
# TODO: Select HTML element and extract image source
# TODO: Write image to folder.

def lefthandedtoons(start_comic, end_comic):
    HOST = 'https://www.lefthandedtoons.com/'
    CSS = '.comicimage'
    FUNCTION = inspect.stack()[0][3]
    ERROR_FILE = f'{FUNCTION}_errors.txt'
    
    # Creates directory to store comics.
    os.makedirs(f'./{FUNCTION}', exist_ok=True)
    
    for url_number in range(start_comic, end_comic):
        # Downloads page.
        page = f'{HOST}/{url_number}'        
        print(f'Downloading page: {page}...')
        try:
            res = requests.get(page)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
        
        except:
            # Writes download errors to file.
            with open(ERROR_FILE, 'a') as fhandle:
                fhandle.write(f'ERROR DOWNLOADING {page}!')
                fhandle.write(traceback.format_exc(), '\n\n')
            continue

        # Searches for image source using CSS selector.
        comic_elem = soup.select(CSS)
        
        if comic_elem == []:
            # Writes CSS selection errors to file.     
            with open(ERROR_FILE, 'a') as fhandle:
                fhandle.write(f'ERROR DOWNLOADING {page}!')
                fhandle.write('CSS SELECTOR RETURNED NOTHING')
        
        else:
            # Extracts image source link from CSS selection.
            comic_url = comic_elem[0].get('src')    
            
            # Downloads the image.
            print(f'Downloading image {comic_url}...')

            try:
                # Save image to folder.
                res = requests.get(comic_url)
                res.raise_for_status()
                with open(f'./{FUNCTION}/{os.path.basename(comic_url)}', 'wb') as fhandle:
                    for chunk in res.iter_content(100000):
                        fhandle.write(chunk)
            
            except:
                # Writes image download errors to file.
                with open(ERROR_FILE, 'a') as fhandle:
                    fhandle.write(f'ERROR DOWNLOADING {comic_url}')
                    fhandle.write(traceback.format_exc(), '\n\n')


def threaded_execution(start, stop, step, function):
    start_time = time.time()
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

threaded_execution(0, 1920, 120, lefthandedtoons)
quit()

'http://www.lefthandedtoons.com/'
path = './{INDEX}'
INDEX = 0 - 2000
css = '.comicimage'
standalone = True

'http://buttersafe.com/'
path = './YYYY/MM/DD/{DATE}'
DATE = '2007/04/03' - '2025/02/06'
css = '#comic > img'
standalone = True

'http://www.savagechickens.com/'
path = './category/cartoons/page/{INDEX}'
INDEX = 0 - 1300
css = 'div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > img'
standalone = True

'http://www.lunarbaboon.com/'
path = './comics/?currentPage={INDEX}'
INDEX = 0 - 200
css = 'div:nth-child(3) > div:nth-child(3) > p:nth-child(1) > span:nth-child(1) > img'
standalone = False, 'Source relative to host site'

'http://www.exocomics.com/'
path = './{INDEX}'
range = 0 - 800
css = '.image-style-main-comic'
standalone = False, 'Source relative to host site'

'http://nonadventures.com/'
path =  './YYYY/MM/DD/{DATE}'
DATE = '2006/09/09' - '2025/02/02'
css = '#comic > img'
standalone = True

'https://squires.nz/'
title_crawl_path = '?comics_paged={INDEX}&blog_paged=1#comics-section'
title_css = 'a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p'
comic_path = './comic/{TITLE}'
INDEX = 1 - 49
TITLE = 'STRING', 'Spaces represented as "-"'

'https://www.sociallyawkwardmisfit.com/'
path = './category/{YEAR}'
YEAR = 2014 - 2024
css = 'div:nth-child(2) > p:nth-child(1) > a'

# NOTE: This is going to be a pain in the ass it seems that the same series wil have different HTML practices among certain images...dammit.