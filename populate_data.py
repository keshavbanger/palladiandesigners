import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palladiun.settings')
django.setup()

from core.models import (
    ProjectCategory, Service, Project, ClientReview, AboutUs,
    TeamMember, FooterContent, Slider, ClientPage, Walkthrough
)

def populate():
    print("Populating database with real assets...")

    # 1. Project Categories
    cat_interior, _ = ProjectCategory.objects.get_or_create(title="Interior Design")
    cat_bim, _      = ProjectCategory.objects.get_or_create(title="BIM Services")
    cat_exterior, _ = ProjectCategory.objects.get_or_create(title="Exterior Design")

    # 2. About Us
    AboutUs.objects.get_or_create(
        heading="Palladian Designers Pvt. Ltd.",
        year=2010,
        text="<p>At Palladian Designers Pvt. Ltd., we transform ideas into reality using cutting-edge BIM technology. With over a decade of combined experience, we deliver world-class interior, exterior, and 3D design solutions — blending creativity with precision.</p>"
    )

    # 3. Services (Matching service cards titles in index.html)
    Service.objects.get_or_create(title="BIM Modeling", description="Detailed Revit models from LOD 100 to 400.")
    # Service cards show fixed static images, but good to have in DB
    Service.objects.get_or_create(title="Interior Design", description="Residential and commercial interiors.")
    Service.objects.get_or_create(title="Exterior Design", description="Facades and outdoor spaces.")
    Service.objects.get_or_create(title="3D Conversion", description="PDF, scan, and point cloud to 3D.")

    # 4. Featured Projects (Using our copied files in media/project_images)
    projects_data = [
        {
            "title": "Modern Living Room",
            "category": cat_interior,
            "year": 2023,
            "description": "A contemporary living room design with sustainable materials and premium finishes.",
            "banner": "project_images/p1.jpg",
            "featured": True,
        },
        {
            "title": "Commercial Office Space",
            "category": cat_interior,
            "year": 2022,
            "description": "High-tech office space for a growing startup, with optimized layouts for productivity.",
            "banner": "project_images/p2.jpg",
            "featured": True,
        },
        {
            "title": "Vila Scan-to-BIM",
            "category": cat_bim,
            "year": 2024,
            "description": "Facade and outdoor design — detailed Scan-to-BIM modeling for a luxury villa in Dubai.",
            "banner": "project_images/p3.jpg",
            "featured": True,
        },
    ]
    for pd in projects_data:
        Project.objects.update_or_create(
            title=pd["title"],
            defaults={
                "project_category": pd["category"],
                "year": pd["year"],
                "description": pd["description"],
                "project_banner_image": pd["banner"],
                "is_featured": pd["featured"],
            }
        )

    # 5. Client Reviews
    ClientReview.objects.update_or_create(
        client_name="Yamini Thota",
        defaults={"feedback": "PDPL transformed our house into a home. Their attention to detail in interior design is unmatched."}
    )
    ClientReview.objects.update_or_create(
        client_name="Supriya Shukla",
        defaults={"feedback": "Working with their BIM team was a seamless experience. The LOD 400 models were precise."}
    )
    ClientReview.objects.update_or_create(
        client_name="Girraj Shrivastava",
        defaults={"feedback": "Facade and outdoor design was exactly like our dream. Professional from start to finish."}
    )

    # 6. Team Members (Chirag removed)
    # TeamMember.objects.get_or_create(
    #     name="Chirag Bhawsar",
    #     designation="Founder & CEO",
    #     social_profile="LinkedIn"
    # )

    # 7. Footer Content
    FooterContent.objects.update_or_create(
        mail="info@palladiandesigners.com",
        defaults={
            "contact_no": "+91 9999999999",
            "short_description": "Global BIM & Engineering firm based in Indore, India.",
            "address": "Indore, Madhya Pradesh 452001"
        }
    )

    # 8. Slider (Main banner)
    Slider.objects.update_or_create(
        is_visible=True,
        defaults={"slider_image": "slider_images/banner1.jpg"}
    )

    # 9. Walkthrough
    Walkthrough.objects.update_or_create(
        project=Project.objects.get(title="Vila Scan-to-BIM"),
        defaults={"video_url": "https://www.youtube.com/embed/ISTpyfaxlxo"}
    )

    print("Success: Database populated with real assets.")

if __name__ == "__main__":
    populate()
