"""
Scraping instructions: 

https://www.reddit.com/r/starcitizen/comments/ab0gja/how_to_download_3d_print_holo_viewer_models/

"""
# TODO: get a requirements.txt going
import datetime as dt
import os
import tempfile
import webbrowser

from bs4 import BeautifulSoup
import PyQt5
import bpy
import requests
import html5lib


# TODO: get URL for RSI webpage
base_url = "https://robertsspaceindustries.com/"

# something like
"https://robertsspaceindustries.com/media/21qi67il3hjrar/source/VANDUUL-Scythe4.ctm" 

# Start scraping
BeautifulSoup

pledge_ships_url = os.path.join(base_url, 'pledge/ships/')
page = requests.get(pledge_ships_url)

# TODO need to find a way to close the banner page that pops up (i think cookies allows this to be suppressed

# with tempfile.TemporaryDirectory() as tmp_dir:
#     tmp_fn = os.path.join(tmp_dir, 'page.html')
#     with open(tmp_fn, 'wb') as f:
#         f.write(page.content)
#     webbrowser.open(tmp_fn)
#     print()


# soup = BeautifulSoup(page.content, "html.parser")
soup = BeautifulSoup(page.content, "html5lib")

print(soup.prettify())

# Find ship links on this page, then iterate over them to get and extract data from each page
search_results = soup.find(id='search-results')

ship_items = search_results.find_all('li')
# TODO: this list is truncated, but gets longer if you scroll, how do make this full?

# TODO: use selenium to load page, use webdriver to scroll (and do anything else), then send this content to beautifulsoup

raise NotImplemented()

# TODO: 
# you have to open the source code (strg + u) then searsch for "ctm" (strg + f) then you find a path in case of the hawk

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
