from django.http import response
from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.profile
                if not profile.bio or not profile.picture:
                    if request.path not in [reverse('users:update'), reverse('users:logout')]:
                        return redirect('users:update')


        response = self.get_response(request)
        return response