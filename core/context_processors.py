from .models import FooterContent
from datetime import datetime

def footer(request):
    current_year = datetime.now().year
    footer_content = FooterContent.objects.first()
    return {"footer_content": footer_content, "current_year": current_year}