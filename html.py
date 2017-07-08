from urllib.request import Request, urlopen
import urllib.request
import re

global htmlCache
htmlCache = [[], []]


def cache_html(url, html):
    htmlCache[0].append(url)
    htmlCache[1].append(html)


def get_html(url):
    # Open the URL
    # Spoof the user agent
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0')
    # Read the response as HTML
    if url in htmlCache[0]:
        # If the URL is in the cache, get its HTML
        return htmlCache[1][htmlCache[0].index(url)]
    try:
        urlopen(request).read()
        html = urlopen(request).read().decode('ascii', 'ignore')
        if len(re.findall('error-desc', html)) > 0:
            return None
        else:
            cache_html(url, html)
            return html
    except urllib.error.HTTPError as err:
        print(f"{err.code} for {url}")
        return None
