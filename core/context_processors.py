from .models import FooterContent


def footer(request):
    footer_content = FooterContent.objects.first()
    return {"footer_content": footer_content,}