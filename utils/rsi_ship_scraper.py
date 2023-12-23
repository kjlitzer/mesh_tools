"""
Tool for automated scraping and mesh editing of SC holoviewer models.

Manual Scraping instructions:
https://www.reddit.com/r/starcitizen/comments/ab0gja/how_to_download_3d_print_holo_viewer_models/
"""

# TODO: get a requirements.txt going
import os
import time
import tempfile
import datetime as dt
import webbrowser
from urllib.parse import urljoin
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import PyQt5
import bpy

# Selenium chrome options
CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"


def scroller(url, scroll_pause_time_sec=1.0):
    """
    Opens URL with selenium, attempts to scroll to bottom of page, then returns soup content

    :param url: String with url for page to open, then scroll
    :param scroll_pause_time_sec: time in seconds to define for time.sleep() between each scroll attempt
    :return: beautifulsoup soup object
    """

    # Configure chrome to be headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)

    try:
        driver.get(url)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # TODO: change this from a crude sleep to either an implicit wait (better, but not ideal)
            #       or and explicit wait (ideal) that specifically checks for the existence of some content
            time.sleep(scroll_pause_time_sec)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup

    except Exception as e:
        print(f"Failed to scroll though web page to load additional dynamic content! Exception: {e}")

    finally:
        driver.quit()


def open_url_in_browser_locally(url):
    """
    Opens page in a web browser using selenium's web driver (for development and debugging purposes).

    :param url: string containing web URL
    :return:
    """

    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(url)

    raise NotImplementedError("!!! this doesn't actually work within a function(?), "
                              "is only here to be copied and pasted in line within script.")


def open_page_in_browser_locally(page):
    """
    Opens page in a web browser, saving HTML locally first rather than requesting it from server.

    :param page: Requests.get() response
    :return:
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_fn = os.path.join(tmp_dir, 'page.html')
        with open(tmp_fn, 'wb') as f:
            f.write(page.content)
        webbrowser.open(tmp_fn)
        print()


def get_ship_3d_model_path_from_page(url):
    """
    Searches through ship page HTML content to find occurences of javascript content that should contain a reference
        to the path that holoviewer uses to dynamically load the 3D model file for the ship in context.

    :param url: Ship page to search for 3D model file reference in.
    :return: string containg the path for the ship model file
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")

    # Search through scripts for reference to *.CTM file
    model_path = ''
    scripts = soup.find_all("script", {'type': 'text/javascript'})
    for script in scripts:
        if len(script) > 0:
            content = ''.join(script.contents)
            if '.ctm' in content or 'model_3d' in content:
                # print(f'Located ship model reference in content: {content}')

                # Use regex matching to extract model path string
                model_string_format = 'model_3d: [\S]+'
                pattern = re.compile(model_string_format)
                matches = pattern.findall(content)

                if len(matches) == 1:
                    model_path = ''.join(matches[0].split(":")[1:]).strip().strip('\'')
                elif len(matches) == 0:
                    RuntimeError("Failed to find scripts content in HTML source when attempting to "
                                 "locate 3D model file paths.")
                else:  # len(matches) > 0
                    RuntimeError(
                        f"Found multiple 3D model file references in HTML source: {matches}.")

                break
        else:
            RuntimeError(
                "Failed to find scripts content in HTML source when attempting to locate 3D model file paths.")

    # Sometimes URL is full, but sometimes it is not
    if "https://" not in model_path:
        full_model_path = urljoin('https://robertsspaceindustries.com', model_path)
    else:
        full_model_path = model_path

    return full_model_path


def main():

    # Start scraping
    base_url = "https://robertsspaceindustries.com/"
    pledge_ships_url = urljoin(base_url, 'pledge/ships/')

    scroll = True
    if not scroll:
        page = requests.get(pledge_ships_url)
        soup = BeautifulSoup(page.content, "html5lib")
    else:
        soup = scroller(pledge_ships_url, scroll_pause_time_sec=1.0)

    # Find ship links on this page, then iterate over them to get and extract data from each page
    search_results = soup.find(id='search-results')
    ship_items = search_results.find_all('li')
    ship_page_urls = []

    for si in ship_items:
        path = si.find(class_='trans-02s').find(class_='trans-02s')["href"]
        ship_page_url = urljoin(base_url, path)
        ship_page_urls.append(ship_page_url)

    print(f"Individual ship page URLs: ({len(ship_page_urls)})")
    for spu in ship_page_urls:
        print(f"{spu}")

    # Go to each page and find the path to the CTM model file in the holoviewer
    with tempfile.TemporaryDirectory(dir=r'C:\Users\kyle\Downloads') as tmp_dir:
        for spu in ship_page_urls:
            ship_name = '_'.join(spu.split('/')[-2:])
            print(f"Attempting to find 3D model download URL for {ship_name}")
            ship_model_url = get_ship_3d_model_path_from_page(spu)
            print(f"Found ship model path for {ship_name}: {ship_model_url}")

            # Download file from path
            print(f"Attempting to download model file for {ship_name} from {ship_model_url}")
            r = requests.get(ship_model_url)
            with open(os.path.join(tmp_dir, f"{ship_name}.ctm"), 'wb') as f:
                f.write(r.content)

            print()

    raise NotImplemented()

    # TODO: convert from CTM to STL? (or OBJ?)

    # TODO: store files on NAS at Z:/
    storage_path = r"Z:\User Data\3d_printing\asset_extraction\SC\holoviewer"

    # TODO: get blender API in here and accessible
    bpy

    # TODO: turn everything into a function

    # TODO: build up a QT GUI for click and get type stuff
    PyQt5

    # TODO: date based directory for saving assets
    # TODO: temporary file storage?
    # TODO: support using pre-existing files?


if __name__ == "__main__":
    main()
