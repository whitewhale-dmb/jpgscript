#!/usr/bin/env python3
import argparse
import io
from PIL import Image
from PIL.ExifTags import TAGS

parser = argparse.ArgumentParser(
                    prog = 'jpgscript.py',
                    description = 'Takes a JavaScript file and embeds it into a JPEG image.',
                    epilog = 'This script takes a JavaScript file and embeds it within a JPEG comment, wrapping the rest of the invalid JPEG bytes in JavaScript comments.')

parser.add_argument('-i', '--image', required=True)           # positional argument
parser.add_argument('-s', '--script', required=True)      # option that takes a value

args = parser.parse_args()

try:
    f = open(args.script, "rb")
    code = f.read()
    f.close()
except Exception as ex:
    print("[!] Error reading script file '%s': %s" % (args.script, ex))
    exit()


try:
    imageData = Image.open(args.image)
    imageBytes = io.BytesIO()
    imageData.save(imageBytes, format='JPEG')
    image = imageBytes.getvalue()
    image = image[20:image.find(b'\xFF\xD9')]

    width = imageData.width.to_bytes(2,'big')
    height = imageData.height.to_bytes(2,'big')
except Exception as ex:
    print("[!] Error reading image file '%s': %s" % (args.image, ex))
    exit()

# JPEG header length 
hlength = 0x093A

header = b'\xFF\xD8\xFF\xE0'+hlength.to_bytes(2, 'big')                         # Marker, APP0, APP0 length
header += b'\x4A\x46\x49\x46\x2F'                                               # "JFIF"+"/" instead of 0x00
header += b'\x2A\x01\x01'                                                       # "*" + 01 + units used for resolution  
header += width                                                                 # Resolution Width 
header += height                                                                # Resolution Height                       
header += b'\x00\x00'                                                           # X + Y pixel count
headerpadding = b'\x00' * (hlength - (len(header)-4))                           # Padding needs to be APP0 length minus header length after the 4 bytes for starting markers,
codestart = b'\xFF\xFE' + (len(code)+7).to_bytes(2, 'big') + b'\x2A\x2F\x3D'    # Comment marker, length + "*/="
codeend = b'\x2F\x2A'                                                           # "/*"
imageend = b'\x2A\x2F\x2F\x2F\xFF\xD9'                                          # "*///" + end-of-image marker

output = header + headerpadding + codestart + code + codeend + image + imageend
outputName = args.script.replace(".","-")+".jpg"

try:
    f = open(outputName, "wb")
    f.write(output)
    f.close()
except Exception as ex:
    print("[!] Error writing output to '%s': %s" % (outputName, ex))
    exit()

print("[+] Polyglot JPEG saved to ./%s" % outputName)
