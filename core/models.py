from typing import Iterable
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django_resized import ResizedImageField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateField(auto_now = True, blank = True, null = True)

    class Meta:
        abstract = True

class Slider(BaseModel):
    slider_image = ResizedImageField(force_format="WEBP", quality=75, upload_to="slider_images/")
    is_visible = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.slider_image.url
    
class Service(BaseModel):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank=True, null=True)


    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ("title",)
    
class ServiceDetail(BaseModel):
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self) -> str:
        return self.service.title

class ProjectCategory(BaseModel):
    title = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("title",)
    
class Project(BaseModel):
    project_category = models.ForeignKey(ProjectCategory, on_delete = models.CASCADE, related_name="project_cat")
    title = models.CharField(max_length = 100)
    slug = models.SlugField(unique=True, blank=True)
    is_featured = models.BooleanField(default=False)
    year = models.IntegerField()
    description = models.TextField()
    project_banner_image = ResizedImageField(force_format="WEBP", quality=75, upload_to="project_images/")

    def save(self, *args, **kwargs):
        # Generate a slug if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.title)

            # Ensure the slug is unique
            original_slug = self.slug
            count = 1
            while Project.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1

        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title

class Walkthrough(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    video_url = models.URLField()


    def __str__(self) -> str:
        return self.project.title
    
class ProjectImage(BaseModel):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    project_image = ResizedImageField(force_format="WEBP", quality=75, upload_to="project_images/")

    is_project_last_image = models.BooleanField(default = False)
    project_short_des = models.TextField(blank = True, null = True, help_text='Fill this field if is project last image is checked!',)


    def __str__(self) -> str:
        return self.project.title

class ClientReview(BaseModel):
    client_name = models.CharField(max_length = 50)
    feedback = models.TextField()
    # client_img = models.ImageField(upload_to="client_images/")


    def __str__(self) -> str:
        return self.client_name
    
class ContactForm(BaseModel):
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    mobile_no = models.CharField(max_length = 15)
    message = models.TextField()


    def __str__(self) -> str:
        return self.name

class AboutUs(models.Model):
    heading = models.CharField(max_length = 100)
    year = models.IntegerField()
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self) -> str:
        return self.heading
    
class TeamMember(BaseModel):
    name = models.CharField(max_length = 50)
    image = ResizedImageField(force_format="WEBP", quality=75, upload_to="team_members/")
    social_profile = models.CharField(max_length = 50, blank=True, null=True)
    designation = models.CharField(max_length = 50)


    def __str__(self) -> str:
        return self.name
    
class FooterContent(BaseModel):
    mail = models.CharField(max_length = 50)
    contact_no = models.CharField(max_length = 15)
    short_description = models.TextField()
    address = models.TextField()

    def __str__(self) -> str:
        return self.mail
    
class PricingPlan(BaseModel):
    project_category = models.ForeignKey(ProjectCategory, on_delete = models.CASCADE)
    price = models.IntegerField()
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self) -> str:
        return self.project_category.title
    
class ClientPage(BaseModel):
    client_logo = ResizedImageField(force_format="WEBP", quality=75, upload_to="clients_images/")
    client_name = models.CharField(max_length = 50)
    client_site = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.client_name