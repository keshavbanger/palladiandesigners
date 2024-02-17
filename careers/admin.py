from django.contrib import admin
from .models import Career, JobDetail, CandidateProfile

# Register your models here.
class CareerAdmin(admin.ModelAdmin):
    list_display = ["job_title", "location", "is_active"]
    prepopulated_fields = {"slug": ["job_title"]}


admin.site.register(Career, CareerAdmin)
admin.site.register(JobDetail)
admin.site.register(CandidateProfile)