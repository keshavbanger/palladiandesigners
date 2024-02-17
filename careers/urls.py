from django.urls import path, include
from .views import careers_page, job_detail

urlpatterns = [
    path('', careers_page, name="careers_page"),
    path('job_detail/<str:career_id>', job_detail, name="job_detail"),
]