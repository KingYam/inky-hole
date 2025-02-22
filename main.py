import os
import json
from sys import exit
import requests
from dotenv import load_dotenv

from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# Set current directory

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load graphic

img = Image.open("./logo.png")
draw = ImageDraw.Draw(img)

# Get app password from .env (new for V6, no more api key)
load_dotenv()
env_password = os.getenv("PASSWORD")

# Setup new V6 api URLs and pass app password for auth
auth_url = 'http://192.168.50.140/api/auth'
auth_data = { 'password': env_password }
stats_url = 'http://192.168.50.140/api/stats/summary'

# Make requests, use sid in response from auth, pass as header for stats get request 
session = requests.Session()
r1 = session.post(auth_url, json=auth_data)
auth_json = r1.json()
sid = auth_json['session']['sid']
r2 = session.get(stats_url, headers={'sid': sid})

# Parse JSON returned from get request above
parsed_json = r2.json()
adsblocked = parsed_json['queries']['blocked']
ratioblocked = parsed_json['queries']['percent_blocked']

session.close()

# Render on hat
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
inky_display.h_flip = True
inky_display.v_flip = True

inky_display.set_image(img)

inky_display.show()
