import os
import re
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palladiun.settings')
django.setup()

from core.models import TeamMember
from django.core.files.base import ContentFile
req = urllib.request.Request('https://palladiandesigners.com/about-us/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Pattern for the live site HTML structure
pattern = r'<div class="team-outer.*?<img.*?src="([^"]+)".*?</div>.*?<div class="name".*?<h3[^>]*>(.*?)</h3>.*?<h3[^>]*>(.*?)</h3>'

matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

print(f"Found {len(matches)} team members in the HTML.")

for img_url, name, designation in matches:
    name = name.strip()
    designation = designation.strip()
    img_url = img_url.strip()
    if img_url.startswith('/'):
        img_url = f"https://palladiandesigners.com{img_url}"
    
    # Check if already exists
    if TeamMember.objects.filter(name=name).exists():
        print(f"Skipping {name}, already exists")
        continue
    
    print(f"Adding {name} - {designation}...")
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        img_data = urllib.request.urlopen(req).read()
        filename = img_url.split('/')[-1]
        
        member = TeamMember(name=name, designation=designation)
        member.image.save(filename, ContentFile(img_data), save=True)
    except Exception as e:
        print(f"Error for {name}: {e}")
