from django.contrib import admin
from .models import CurrentOpenning, JobOpeningDetail, AppliedCandidateProfile

# Register your models here.
class CurrentOpenningAdmin(admin.ModelAdmin):
    list_display = ["job_title", "location", "is_active"]
    prepopulated_fields = {"slug": ["job_title"]}


admin.site.register(CurrentOpenning, CurrentOpenningAdmin)
admin.site.register(JobOpeningDetail)
admin.site.register(AppliedCandidateProfile)