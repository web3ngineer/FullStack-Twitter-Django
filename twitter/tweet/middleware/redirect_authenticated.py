from django.shortcuts import redirect

import logging
logger = logging.getLogger(__name__)

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/accounts/login/':
            previous_url = request.META.get('HTTP_REFERER', '/tweet')
            logger.info(f"Redirecting authenticated user to {previous_url}")
            return redirect(previous_url)
        
        return self.get_response(request)
