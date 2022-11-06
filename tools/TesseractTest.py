import pytesseract
from PIL import ImageGrab
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#1577, 105
#1604, 141

im = ImageGrab.grab(bbox=(1671, 48, 1769, 121))

for x in range(im.width):
    for y in range(im.height):
        color = im.getpixel((x, y))
        if sum(color) > 500:
            im.putpixel((x, y), (255,255,255))
        else:
            im.putpixel((x, y), (1, 1, 1))
im.save('C:\\Users\\Evan Goldman\\Downloads\\' + "test" + r'.png')
toStr = pytesseract.image_to_string(im, config='--psm 7') #-c tessedit_char_whitelist=0123456789oOlLiI
print(toStr)