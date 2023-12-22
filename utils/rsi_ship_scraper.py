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

import requests
import html5lib
from bs4 import BeautifulSoup
from selenium import webdriver
import PyQt5
import bpy


def scroller(url, scroll_pause_time_sec=1.0):
    """
    Opens URL with selenium, attempts to scroll to bottom of page, then returns soup content

    :param url: String with url for page to open, then scroll
    :param scroll_pause_time_sec: time in seconds to define for time.sleep() between each scroll attempt
    :return: beautifulsoup soup object
    """

    driver = webdriver.Chrome()
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
    Opens page in a web browser using selenium's web driver.

    :param url: string containing web URL
    :return:
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(url)


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


def main():

    # Start scraping
    base_url = "https://robertsspaceindustries.com/"
    # pledge_ships_url = os.path.join(base_url, 'pledge/ships/')
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
        # ship_page_url = base_url + '/' + str(path)
        ship_page_url = urljoin(base_url, path)
        ship_page_urls.append(ship_page_url)

    print(f"Individual ship page URLs: ({len(ship_page_urls)})")
    for spu in ship_page_urls:
        print(f"{spu}")

    # Go to each page and find the path to the CTM model file in the holoviewer
    for spu in ship_page_urls:
        print(f"Attempting to fetching model for {spu.split('/')[-1]}")

        open_url_in_browser_locally(spu)

        print()
        page = requests.get(spu)
        soup = BeautifulSoup(page.content, "html5lib")


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
