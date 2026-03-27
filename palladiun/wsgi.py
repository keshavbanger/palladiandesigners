"""
WSGI config for palladiun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palladiun.settings')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # WhiteNoise bypass for Vercel: forcibly serve Media files through Python since Vercel's static router fails on media folders without @vercel/static
    from whitenoise import WhiteNoise
    from django.conf import settings
    application = WhiteNoise(application, root=settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
    
    app = application
except Exception as e:
    import traceback
    error_msg = f"Django Vercel Crash: {str(e)}\n\n" + traceback.format_exc()
    
    def application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [error_msg.encode('utf-8')]
    
    app = application
