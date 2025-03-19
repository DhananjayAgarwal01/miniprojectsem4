from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from ..models import UserProfile, Donation, PickupRequest

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(View):
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('landing')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('landing')

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create UserProfile with proper error handling
            user_type = request.POST.get('user_type', 'RECIPIENT')
            if user_type not in ['DONOR', 'RECIPIENT']:
                user_type = 'RECIPIENT'  # Default fallback
                
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                profile_info=request.POST.get('profile_info', '')
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {
        'form': form,
        'user_types': [
            ('DONOR', 'Donor'),
            ('RECIPIENT', 'Recipient')
        ]
    })

@login_required
def profile(request):
    """User profile view."""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create a default profile if it doesn't exist
        user_profile = UserProfile.objects.create(
            user=request.user,
            user_type='RECIPIENT'  # Default type
        )
        messages.info(request, 'A default profile has been created for you. Please update your information.')
    
    context = {
        'profile': user_profile,
        'donation_count': user_profile.user.donations.count(),
        'request_count': user_profile.user.pickup_requests.count(),
        'completed_count': user_profile.user.pickup_requests.filter(status='COMPLETED').count(),
        'donations': user_profile.user.donations.order_by('-donation_date')[:6],
        'requests': user_profile.user.pickup_requests.order_by('-request_date')[:6]
    }
    return render(request, 'chat/profile.html', context)

@login_required
def profile_edit(request):
    """Edit profile view."""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(
            user=request.user,
            user_type='RECIPIENT'
        )
        messages.info(request, 'A default profile has been created for you.')
    
    if request.method == 'POST':
        try:
            user = request.user
            
            # Update user email
            email = request.POST.get('email', '').strip()
            if email and email != user.email:
                try:
                    user.email = email
                    user.save()
                except Exception as e:
                    messages.error(request, 'Failed to update email. Please try again.')
                    return render(request, 'chat/profile_edit.html', {
                        'user': request.user,
                        'user_profile': user_profile
                    })
            
            # Update profile fields
            user_profile.phone = request.POST.get('phone', '').strip()
            user_profile.location = request.POST.get('location', '').strip()
            user_profile.profile_info = request.POST.get('profile_info', '').strip()
                
            user_profile.email_notifications = request.POST.get('email_notifications') == 'on'
            
            user_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('chat:profile')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'chat/profile_edit.html', {
        'user': request.user,
        'user_profile': user_profile
    })


def landing_page(request):
    """Landing page for non-authenticated users."""
    if request.user.is_authenticated:
        return redirect('chat:dashboard')
    return render(request, 'landing.html')

@login_required
def home(request):
    """Home page for authenticated users."""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user_profile': user_profile,
        'recent_donations': Donation.objects.order_by('-donation_date')[:6],
        'donation_requests': PickupRequest.objects.filter(
            donation__donor=request.user
        ).order_by('-request_date')[:5]
    }
    return render(request, 'chat/home.html', context)

@login_required
def dashboard(request):
    """User dashboard view."""
    user_profile = request.user.userprofile
    
    # Get user's donations or requests based on user type
    if user_profile.user_type == 'DONOR':
        donations = Donation.objects.filter(
            donor=request.user
        ).select_related('category').order_by('-donation_date')[:5]
        
        requests = PickupRequest.objects.filter(
            donation__donor=request.user
        ).select_related('donation', 'recipient').order_by('-request_date')[:5]
    else:
        donations = Donation.objects.filter(
            recipient=request.user
        ).select_related('category').order_by('-donation_date')[:5]
        
        requests = PickupRequest.objects.filter(
            recipient=request.user
        ).select_related('donation', 'donation__donor').order_by('-request_date')[:5]
    
    return render(request, 'chat/dashboard.html', {
        'donations': donations,
        'requests': requests,
        'user_profile': user_profile
    })