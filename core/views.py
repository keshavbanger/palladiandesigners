from django.shortcuts import render, redirect
from core.models import Slider, Project, ClientReview, AboutUs, TeamMember, ProjectCategory, ProjectImage, Service, ContactForm, PricingPlan, ClientPage, ServiceDetail
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def index(request):
    slider_img = Slider.objects.filter(is_visible = True).last()
    projects = Project.objects.all().order_by("-year")
    testimonials = ClientReview.objects.all().order_by('-created_at')
    about = AboutUs.objects.all().first()
    year = about.year
    context = {
        "slider_img": slider_img,
        "projects": projects,
        "testimonials": testimonials,
        "about": about,
        "total_company_years": year,
    }
    return render(request, 'index.html', context)

def about_us(request):
    team_members = TeamMember.objects.all()
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
    return render(request, 'work-grid.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project_cat = project.project_category.title
    title = project.title
    project_images = ProjectImage.objects.filter(project=project).select_related('project')
    context = {
        "images": project_images,
        "project_cat": project_cat.upper(),
        "title": title,
        "project": project,
    }
    return render(request, 'project_details.html', context)


def services(request):
    services = Service.objects.all()
    context = {
        "services": services
    }
    return render(request, 'services.html', context)


def contact_us(request):
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
        res = send_mail_admin(name, email, mobile_no, message)
        print("Mail Sent Successfully")
        return redirect("contactus")
    return render(request, 'contact-us.html')

def send_mail_admin(name, email, mobile_no, message):
    html_content = render_to_string('static/emails/contact_email.html', {'name': name, 'email': email, 'message': message})
    text_content = strip_tags(html_content)
    # admin_email = "harshit.s@goldeneagle.ai"
    admin_email = "harshitshreshthi8@gmail.com"
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
    client_pages = ClientPage.objects.all()
    context = {
        "client_pages": client_pages,
        "header_dark": "dark",
        "show_filter": False
    }
    return render(request, 'clients.html', context)

def service_detail(request, id):
    try:
        service_detail = ServiceDetail.objects.get(id = id)
    except ServiceDetail.DoesNotExist:
        return render(request, '404.html')
    context = {
        "service_detail": service_detail
    }
    return render(request, 'services_details.html', context)