from urllib.request import Request, urlopen
import urllib.request
import re


def get_html(url):
    # Open the URL
    # Spoof the user agent
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0')
    # Read the response as HTML
    try:
        urlopen(request).read()
        html = urlopen(request).read().decode('ascii', 'ignore')
        if len(re.findall('error-desc', html)) > 0:
            return None
        else:
            return html
    except urllib.error.HTTPError as err:
        print(f"{err.code} for {url}")
        return None
