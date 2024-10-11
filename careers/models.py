from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
import uuid
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateField(auto_now = True, blank = True, null = True)

    class Meta:
        abstract = True


def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value.size > limit:
        raise ValidationError(_('File size must be no more than 2 MB.'))

class CurrentOpenning(BaseModel):
    job_title = models.CharField(max_length = 100)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(default = "INDORE", max_length = 20)
    is_active = models.BooleanField(default = True)

    def save(self, *args, **kwargs):
        # Generate a slug if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.title)

            # Ensure the slug is unique
            original_slug = self.slug
            count = 1
            while CurrentOpenning.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1

        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.job_title
    
class JobOpeningDetail(BaseModel):
    job = models.ForeignKey(CurrentOpenning, on_delete = models.CASCADE)
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self) -> str:
        return self.job.job_title

class AppliedCandidateProfile(BaseModel):
    job_detail = models.ForeignKey(JobOpeningDetail, on_delete = models.CASCADE)
    candidate_resume = models.FileField(upload_to="candidate_resume/", validators=[validate_file_size])
    candidate_portfolio = models.FileField(upload_to="candidate_portfolio/", blank = True, null = True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique = True)
    phone_number = models.CharField(max_length = 15)
    current_location = models.CharField(max_length = 50)
    notice_period = models.CharField(max_length = 50)
    current_ctc = models.CharField(max_length = 20)
    expected_ctc = models.CharField(max_length = 20)



    def __str__(self) -> str:
        return f"{self.job_detail.job} - {self.first_name} {self.last_name}"


