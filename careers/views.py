from django.shortcuts import render
from .models import CurrentOpenning, JobOpeningDetail, AppliedCandidateProfile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your views here.
def careers_page(request):
    careers = CurrentOpenning.objects.filter(is_active = True).order_by("created_at")
    context = {
        "careers": careers
    }
    return render(request, "careers_page.html", context)

def send_mail_to_admin(first_name, last_name, email, phone_number, position_name):
    html_content = render_to_string('static/emails/candidate_applied.html', {'first_name': first_name, 'last_name':last_name, 'email': email, "mobile_no": phone_number, 'position_name': position_name})
    text_content = strip_tags(html_content)
    admin_email = "services@palladiandesigners.com"
    # admin_email = "services@palladiandesigners.com"
    msg = EmailMultiAlternatives(
        'Candidate Applied - Palladian Designers',
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

def job_detail(request, career_id):
    is_successful_applied = False

    if request.method == "POST":
        job_career_detail = request.POST.get("job_career_detail")
        job_candidate_detail = JobOpeningDetail.objects.get(id=job_career_detail)
        # Rest of your code remains unchanged
        job_career_detail = request.POST.get("job_career_detail")
        job_candidate_detail = JobOpeningDetail.objects.get(id = job_career_detail)
        first_name = request.POST.get("first_name")
        candidate_resume = request.FILES["candidate_resume"]
        candidate_portfolio = request.FILES["candidate_portfolio"]
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        current_location = request.POST.get("current_location")
        notice_period = request.POST.get("notice_period")
        current_ctc = request.POST.get("current_ctc")
        expected_ctc = request.POST.get("expected_ctc")
        position_name = request.POST.get("position_name")
        try:
            candidate = AppliedCandidateProfile(
                job_detail=job_candidate_detail,
                candidate_resume=candidate_resume,
                candidate_portfolio=candidate_portfolio,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                current_location=current_location,
                notice_period=notice_period,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc
            )
            candidate.save()
            print("Candidate Applied Successfully!")
            is_successful_applied = True
            send_mail_to_admin(first_name, last_name, email, phone_number, position_name)
        except Exception as e:
            context = {
                "is_applied_before": True,
            }
            print("You already Applied for this JOB.", str(e))
            return render(request, 'job_details.html', context)

    try:
        job_career_detail = JobOpeningDetail.objects.get(job__id=career_id)
    except JobOpeningDetail.DoesNotExist:
        return render(request, '404.html', {"header_dark": "dark"})

    context = {
        "job_career_detail": job_career_detail,
        "applied_successful": is_successful_applied,
    }
    return render(request, 'job_details.html', context)


