from django.contrib import admin
from .models import CurrentOpenning, JobOpeningDetail, AppliedCandidateProfile
from django.contrib.admin import RelatedOnlyFieldListFilter

# Register your models here.
class CurrentOpenningAdmin(admin.ModelAdmin):
    list_display = ["job_title", "location", "is_active"]
    prepopulated_fields = {"slug": ["job_title"]}


class AppliedCandidateProfileAdmin(admin.ModelAdmin):
    list_display = ["full_name", "current_ctc", "expected_ctc", "current_location", "notice_period", "created_at"]
    ordering = ("-created_at",)
    list_per_page = 20
    list_filter = ("job_detail",)  # Add filters for these fields
    search_fields = ["first_name", "last_name", "current_location", "email"]  # Add search functionality

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    full_name.short_description = 'Name'

admin.site.register(CurrentOpenning, CurrentOpenningAdmin)
admin.site.register(JobOpeningDetail)
admin.site.register(AppliedCandidateProfile, AppliedCandidateProfileAdmin)