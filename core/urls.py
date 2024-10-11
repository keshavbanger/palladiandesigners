from django.urls import path, include
from .views import index, about_us, projects, project_detail_view, services, contact_us, pricing_plan, clients, service_detail, project_view


urlpatterns = [
    path('', index, name="index"),
    path('about-us/', about_us, name="about"),
    path('projects/', projects, name="projects"),
    path('projects-details/<slug:slug>/', project_detail_view, name="project-details"),
    path('project-cat/<int:cat_id>/', project_view, name="project-cat"),
    path('services/', services, name="services"),
    path('contact-us/', contact_us, name="contactus"),
    path('pricing-plan/', pricing_plan, name="pricing-plan"),
    path('clients/', clients, name="clients"),
    path('service_detail/<int:id>/', service_detail, name="service_detail"),
]