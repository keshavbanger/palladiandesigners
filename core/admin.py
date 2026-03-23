from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import *
import os

class SliderAdmin(admin.ModelAdmin):
    list_display = ("slider_image_tag", "is_visible", "created_at", "updated_at")
    ordering = ("-created_at",)
    def slider_image_tag(self, obj):
        folder_path = 'media/slider_images'
        file_name = obj.slider_image.url.split("/")[3]
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return format_html(f'<img src="{obj.slider_image.url}" width="80" height="80" />')
        return format_html(f'<img src="{settings.BASE_URL}/{folder_path}/default_img.png" width="80" height="80" />')
    slider_image_tag.short_description = 'Slider Image'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_category", "title", "project_image_tag")
    prepopulated_fields = {"slug": ["title"]}
    ordering = ("-created_at",)
    def project_image_tag(self, obj):
        folder_path = 'media/project_images'
        file_name = obj.project_banner_image.url.split("/")[3]
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return format_html(f'<img src="{obj.project_banner_image.url}" width="80" height="80" />')
        return format_html(f'<img src="{settings.BASE_URL}/{folder_path}/default_img.png" width="80" height="80" />')
    project_image_tag.short_description = 'Project Image'


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "mobile_no", "created_at"]


class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "project_image_tag")
    ordering = ("-created_at",)
    def project_image_tag(self, obj):
        folder_path = 'media/project_images'
        file_name = obj.project_image.url.split("/")[3]
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return format_html(f'<img src="{obj.project_image.url}" width="80" height="80" />')
        return format_html(f'<img src="{settings.BASE_URL}/{folder_path}/default_img.png" width="80" height="80" />')

admin.site.register(Slider, SliderAdmin)
admin.site.register(Service)
admin.site.register(ProjectCategory)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ClientReview)
admin.site.register(ContactForm, ContactFormAdmin)
admin.site.register(ProjectImage, ProjectImageAdmin)
admin.site.register(AboutUs)
admin.site.register(TeamMember)
admin.site.register(FooterContent)
admin.site.register(PricingPlan)
admin.site.register(ClientPage)
admin.site.register(ServiceDetail)
admin.site.register(Walkthrough)