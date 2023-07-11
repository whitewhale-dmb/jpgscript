# jpegscript.py

## About
This is a simple script for embedding a JavaScript payload within a JPEG file, a.k.a a polyglot JPEG. 
Polyglot JPEGs can be thought of similarly to alternative data streams, allowing the file to function as both a valid JPEG and JavaScript file.

## Use Case
Polyglot JPEGs are useful for sites that contain an XSS vulnerability, but also have:
- a Content Security Policy blocking inline JS
- a Content Security Policy blocking external resources or only external images
- no facilities to upload a conventional JavaScript file
- facilities to upload a JPEG image if external images are blocked by CSP

## How to use
Install requirements:

```pip3 install -r requirements.txt```

Generate a polyglot JPEG:

```python3 jpegscript.py --image <base jpeg file> --script <script to embed>```

Execution via XSS (charset attribute is important):

```<script type="text/javascript" charset="ISO-8859-1" src="/api/avatar/j.smith"></script>```

## Limitations
- The JPEGs extensively use JavaScript comments to prevent invalid character errors. If you have comments in the JS payload, you will need to ensure they're closed off or removed from the file to prevent unexpected issues.
- Some browsers have been trying to patch image files from being loaded in script tags, however this still appears to work for every browser I've tried at time-of-writing. 

## Other Notes
This was originally developed for a HackTheBox web challenge involving a website with a strict CSP and an avatar upload facility which checked the validity of the images uploaded.
All of the theory and techniques are implemented from Gareth Heyes' article [Bypassing CSP using polyglot JPEGs](https://portswigger.net/research/bypassing-csp-using-polyglot-jpegs) for Portswigger.

A test input JPEG and JS file have been included, along with an example output polyglot JPEG and HTML file to test it in.

> This tool is intended for educational and authorized professional pentesting purposes only.
