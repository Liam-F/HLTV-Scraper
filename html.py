from urllib.request import Request, urlopen
import urllib.request
import re
html_cache = {}


def get_html(url):
    # Open the URL and spoof the user agent
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0')
    # Read the response as HTML
    if url in html_cache:
        # If the URL is in the cache, get its HTML
        return html_cache[url]
    try:
        urlopen(request).read()
        html = urlopen(request).read().decode('ascii', 'ignore')

        # HLTV has a custom error page for HTTP errors
        if len(re.findall('error-desc', html)) > 0 or len(re.findall('error-500', html)) > 0:
            return None
        else:
            # Cache the HTML data and return the HTML
            html_cache[url] = html
            return html

    # Handle any other errors
    except:
        print(f"Error for {url}")
        return None
