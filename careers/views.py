from django.shortcuts import render
from .models import Career, JobDetail, CandidateProfile
from django.shortcuts import get_object_or_404

# Create your views here.
def careers_page(request):
    careers = Career.objects.filter(is_active = True).order_by("-created_at")
    context = {
        "careers": careers
    }
    return render(request, "careers_page.html", context)

def job_detail(request, career_id):
    if request.method == "POST":
        job_career_detail = request.POST.get("job_career_detail")
        job_candidate_detail = JobDetail.objects.get(id = job_career_detail)
        first_name = request.POST.get("first_name")
        candidate_resume = request.FILES["candidate_resume"]
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        current_location = request.POST.get("current_location")
        notice_period = request.POST.get("notice_period")
        current_ctc = request.POST.get("current_ctc")
        expected_ctc = request.POST.get("expected_ctc")

        candidate = CandidateProfile(
            job_detail = job_candidate_detail,
            candidate_resume = candidate_resume,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            current_location = current_location,
            notice_period = notice_period,
            current_ctc = current_ctc,
            expected_ctc = expected_ctc
        )
        candidate.save()
        print("Candidate Applied Successfully!")
    job_career_detail = get_object_or_404(JobDetail, job__id=career_id)
    context = {
        "job_career_detail": job_career_detail
    }
    return render(request, 'job_details.html', context)