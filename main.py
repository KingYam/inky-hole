import os
import json
import urllib3
from sys import exit

from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# Set current directory

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load graphic

img = Image.open("./logo.png")
draw = ImageDraw.Draw(img)

# get api data

http = urllib3.PoolManager()

# CHANGE THIS to your URL for your PiHole, and replace <TOKEN HERE> with your API token
url = 'http://192.168.0.140/admin/api.php?summary&auth=<TOKEN HERE>'

try:
  r = http.request('GET', url)
  if r.status >= 200 or r.status <= 299:
    exit("http request is unsuccessful")
except:
  adsblocked = '?'
  ratioblocked = '?'

parsed_json = json.loads(r.data)
adsblocked = parsed_json['ads_blocked_today']
ratioblocked = parsed_json['ads_percentage_today']

font = ImageFont.truetype(FredokaOne, 32)
font_header = ImageFont.truetype(FredokaOne, 16)

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

draw.text((20,5), str(adsblocked), inky_display.RED, font)
draw.text((20, 35), str("Ads Blocked"), inky_display.BLACK, font_header)

if isinstance(ratioblocked, str):
  draw.text((20,50), f"{ratioblocked}%", inky_display.RED, font)
else:
  draw.text((20,50), f"{ratioblocked:.2f}%", inky_display.RED, font)

draw.text((20,80), str("of all queries"), inky_display.BLACK, font_header)

# For flipping display if mounted
# inky_display.h_flip = True
# inky_display.v_flip = True

inky_display.set_image(img)

inky_display.show()
