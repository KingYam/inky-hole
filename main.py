import os
import json
import urllib2
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# Set current directory

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load graphic

img = Image.open("./logo.png")
draw = ImageDraw.Draw(img)

# get api data

try:
  f = urllib2.urlopen('http://192.168.1.27/admin/api.php')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  adsblocked = parsed_json['ads_blocked_today']
  ratioblocked = parsed_json['ads_percentage_today']
  f.close()
except:
  queries = '?'
  adsblocked = '?'
  ratio = '?'

font = ImageFont.truetype(FredokaOne, 32)
font_header = ImageFont.truetype(FredokaOne, 16)

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

draw.text((20,5), str(adsblocked), inky_display.RED, font)
draw.text((20, 35), str("Ads Blocked"), inky_display.BLACK, font_header)
draw.text((20,50), str("%.1f" % round(ratioblocked,2)) + "%", inky_display.RED, font)
draw.text((20,80), str("of all queries"), inky_display.BLACK, font_header)

inky_display.set_image(img)

inky_display.h_flip = True
inky_display.v_flip = True

inky_display.show()
