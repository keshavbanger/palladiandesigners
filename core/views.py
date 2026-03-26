from django.shortcuts import render, redirect
from core.models import (
    Slider, 
    Project, 
    ClientReview, 
    AboutUs, 
    TeamMember, 
    ProjectCategory, 
    ProjectImage, 
    Service, 
    ContactForm, 
    PricingPlan, 
    ClientPage, 
    ServiceDetail,
    Walkthrough
)
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Q

def index(request):
    slider_img = Slider.objects.filter(is_visible = True).last()
    projects = Project.objects.filter(is_featured=True).order_by("-year")
    testimonials = ClientReview.objects.all().order_by('-created_at')
    about = AboutUs.objects.first()
    top_clients = ClientPage.objects.all()[0:4]
    year = about.year if about else 0
    walkthroughs = Walkthrough.objects.all().first()
    context = {
        "slider_img": slider_img,
        "projects": projects,
        "testimonials": testimonials,
        "about": about,
        "total_company_years": year,
        "top_clients": top_clients,
        "walkthrough": walkthroughs
    }
    return render(request, 'index.html', context)

def about_us(request):
    team_members = TeamMember.objects.all().order_by("created_at")
    context = {
        "team_members": team_members
    }
    return render(request, 'about-us.html', context)


def projects(request):
    projects = Project.objects.all()
    project_cat = ProjectCategory.objects.all()
    
    context = {
        "projects": projects,
        "header_dark": "dark",
        "show_filter": True,
        "project_cat": project_cat
    }

    category_ids = [request.GET.get(f'filter_val{i}') for i in range(1, len(project_cat))]
    category_ids = [cat_id for cat_id in category_ids if cat_id is not None and cat_id.isdigit()]

    if category_ids:
        project_cat_inside = ProjectCategory.objects.filter(id__in=category_ids)
        projects = Project.objects.filter(project_category__in=project_cat_inside)

        context["projects"] = projects
        context["project_cat"] = project_cat

    return render(request, 'work-grid.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    walk_through = Walkthrough.objects.filter(project=project)
    project_cat = project.project_category.title
    title = project.title
    project_images = ProjectImage.objects.filter(project=project).select_related('project')
    if project_images.exists():
        last_image = project_images.last()
        # Check if the last image has the attribute is_project_last_image
        if hasattr(last_image, "is_project_last_image") and last_image.is_project_last_image:
            project_image_desc = last_image.project_short_des
        else:
            project_image_desc = ""
    else:
        project_image_desc = ""
    context = {
        "images": project_images,
        "project_cat": project_cat.upper(),
        "title": title,
        "project": project,
        "header_dark": "dark",
        "project_image_desc": project_image_desc,
        "total_image": len(project_images),
        "videos": walk_through,
    }
    return render(request, 'project_details.html', context)


def services(request):
    services = Service.objects.all().order_by("-created_at")
    context = {
        "services": services
    }
    return render(request, 'services.html', context)


def contact_us(request):
    show_msg = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile_no = request.POST.get("phone")
        message = request.POST.get("message")
        contact_form = ContactForm(
            name = name,
            email = email,
            mobile_no = mobile_no,
            message = message
        )
        contact_form.save()
        send_mail_admin(name, email, mobile_no, message)
        show_msg = True
        print("Mail Sent Successfully")
        return render(request, 'contact-us.html', {"show_msg": show_msg})
    return render(request, 'contact-us.html', {"show_msg": show_msg})

def send_mail_admin(name, email, mobile_no, message):
    html_content = render_to_string('static/emails/contact_email.html', {'name': name, 'email': email, "mobile_no": mobile_no, 'message': message})
    text_content = strip_tags(html_content)
    # admin_email = "harshit.s@goldeneagle.ai"
    admin_email = "shivamsdixit23@gmail.com"
    msg = EmailMultiAlternatives(
        'User Contact Query Message',
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def pricing_plan(request):
    pricing_plan = PricingPlan.objects.all()
    context = {
        "pricing_plan": pricing_plan
    }
    return render(request, 'pricing-simple.html', context)


def clients(request):
    client_pages = ClientPage.objects.all().order_by("-created_at")
    context = {
        "client_pages": client_pages,
        "header_dark": "dark",
        "show_filter": False
    }
    return render(request, 'clients.html', context)

def service_detail(request, id):
    try:
        service_detail = ServiceDetail.objects.get(service__id = id)
    except ServiceDetail.DoesNotExist:
        return render(request, '404.html', {"header_dark": "dark"})
    context = {
        "service_detail": service_detail
    }
    return render(request, 'services_details.html', context)

def project_view(request, cat_id):
    projects = Project.objects.filter(project_category__id = cat_id)
    context = {
        "project_cat": projects,
        "header_dark": True,
    }
    return render(request, 'project.html', context)