from django.shortcuts import redirect

class LogoutRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is logged out and trying to access a protected page
        if not request.user.is_authenticated and response.status_code == 404:
            return redirect('login')  # Redirect to the login page or any other desired page

        return response
