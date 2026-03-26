import os
import django
import urllib.request
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palladiun.settings')
django.setup()

from core.models import ProjectCategory, Project
from django.core.files.base import ContentFile

# Category mappings found from live site layout:
# /project-cat/2/ -> ARCHITECTURE
# /project-cat/3/ -> BIM
# /project-cat/1/ -> INTERIOR
# /project-cat/4/ -> LANDSCAPE
# /project-cat/5/ -> STRUCTURE

cat_map_rules = {
    '/project-cat/2/': 'ARCHITECTURE',
    '/project-cat/3/': 'BIM',
    '/project-cat/1/': 'INTERIOR',
    '/project-cat/4/': 'LANDSCAPE',
    '/project-cat/5/': 'STRUCTURE',
}

url = "https://palladiandesigners.com/projects/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    cat_urls = re.findall(r'<a[^>]+href="([^"]+)"[^>]+class="prague-services-link[^"]*"', html)
    
    # We will use to map the LIVE URLs back to our formal 5 DB categories
    db_cats = {c.title: c for c in ProjectCategory.objects.all()}

    for cat_url in set(cat_urls):
        orig_cat_url = cat_url
        if cat_url.startswith('/'):
            cat_url = f"https://palladiandesigners.com{cat_url}"
        
        assigned_title = cat_map_rules.get(orig_cat_url)
        if not assigned_title:
            continue
            
        category_model = db_cats.get(assigned_title)
        if not category_model:
            print(f"Skipping {assigned_title}, not in DB")
            continue
        
        print(f"\n--- Scraping Category: {assigned_title} ---")
        try:
            req_cat = urllib.request.Request(cat_url, headers={'User-Agent': 'Mozilla/5.0'})
            cat_html = urllib.request.urlopen(req_cat).read().decode('utf-8')
            
            # Find projects
            projects = re.findall(r'<h4 class="project-grid-item-title"><a[^>]*>(.*?)</a></h4>', cat_html)
            images = re.findall(r'<div class="project-grid-item-img">\s*<img src="([^"]+)"', cat_html)
            
            for i, p_name in enumerate(projects):
                p_name = p_name.strip()
                img_url = images[i] if i < len(images) else ""
                
                if not img_url:
                    continue
                
                if img_url.startswith('/'):
                    img_url = f"https://palladiandesigners.com{img_url}"
                
                # Create project if not exist
                if not Project.objects.filter(title=p_name).exists():
                    print(f"Adding Project: {p_name}")
                    
                    try:
                        req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                        img_data = urllib.request.urlopen(req_img).read()
                        filename = img_url.split('/')[-1]
                        
                        proj = Project(
                            title=p_name,
                            project_category=category_model,
                            is_featured=True,
                            year="2024"
                        )
                        proj.project_banner_image.save(filename, ContentFile(img_data), save=True)
                    except Exception as e:
                        print(f" Failed to download image for {p_name}: {e}")
                else:
                    print(f"Project {p_name} exists.")
                    
        except Exception as e:
            print("Error loading category:", e)
except Exception as e:
    print("Error:", e)

print("Finished importing projects.")
