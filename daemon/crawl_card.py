"""
https://stackoverflow.com/a/51517606
"""
from selenium.webdriver import Chrome, ChromeOptions
import io
from PIL import Image
import time

SELENIUM_DRIVER_PATH = '/Users/mark/Downloads/chromedriver_mac64 (1)/chromedriver'
SELENIUM_CARD_URL = 'http://localhost:3000/heroes/card'

options = ChromeOptions()
options.add_argument(f"--force-device-scale-factor=2")
options.add_argument(f"--high-dpi-support=1")
options.add_argument("--start-maximized")

chrome = Chrome(SELENIUM_DRIVER_PATH, options=options)
chrome.get(SELENIUM_CARD_URL)
time.sleep(5)
chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

ele = chrome.find_element('id', "render")
print({"location": ele.location, "size": ele.size, "rect": ele.rect})
image = ele.screenshot_as_png

img = Image.open(io.BytesIO(image))
print({"img_size": img.size})
img.save(f"image-{int(time.time())}.png")
