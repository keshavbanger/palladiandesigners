import urllib.request
import re

url = "https://palladiandesigners.com/projects/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # Find category links
    parts = re.findall(r'<a[^>]+href="([^"]+)"[^>]+class="prague-services-link[^"]*"', html)
    print("Found category links:", parts)
except Exception as e:
    print("Error:", e)
