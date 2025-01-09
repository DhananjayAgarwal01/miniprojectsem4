from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def donor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'DONOR':
            messages.error(request, 'Access denied. Donor privileges required.')
            return redirect('chat:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def recipient_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'RECIPIENT':
            messages.error(request, 'Access denied. Recipient privileges required.')
            return redirect('chat:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view 