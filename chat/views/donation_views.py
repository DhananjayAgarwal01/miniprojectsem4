from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from ..models import Donation, Category, PickupRequest, DirectMessage
from ..decorators import donor_required, recipient_required
from ..forms import DonationForm

@login_required
def donation_list(request):
    """List all available donations with filters."""
    donations = Donation.objects.filter(status='AVAILABLE').select_related('donor', 'category')
    categories = Category.objects.all()
    
    # Apply filters
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    query = request.GET.get('q')
    
    if category:
        donations = donations.filter(category__id=category)
    if condition:
        donations = donations.filter(condition=condition)
    if query:
        donations = donations.filter(
            Q(item_name__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Order by donation date
    donations = donations.order_by('-donation_date')
    
    # Pagination
    paginator = Paginator(donations, 12)
    page = request.GET.get('page')
    donations = paginator.get_page(page)
    
    return render(request, 'chat/donation_list.html', {
        'donations': donations,
        'categories': categories,
        'selected_category': category,
        'selected_condition': condition,
        'search_query': query,
        'user_profile': request.user.userprofile
    })

@login_required
@donor_required
def donation_create(request):
    """Create a new donation."""
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(request, 'Donation created successfully!')
            return redirect('chat:donation_detail', pk=donation.pk)
    else:
        form = DonationForm()
    
    return render(request, 'chat/donation_form.html', {
        'form': form,
        'user_profile': request.user.userprofile
    })

@login_required
def donation_detail(request, pk):
    """Display donation details and related requests."""
    donation = get_object_or_404(
        Donation.objects.select_related('donor', 'category'),
        pk=pk
    )
    
    # Get pickup requests if user is the donor
    requests = None
    if request.user == donation.donor:
        requests = PickupRequest.objects.filter(
            donation=donation
        ).select_related('recipient').order_by('-request_date')
    
    # Get similar donations
    similar_donations = Donation.objects.filter(
        status='AVAILABLE',
        category=donation.category
    ).exclude(pk=donation.pk)[:3]
    
    return render(request, 'chat/donation_detail.html', {
        'donation': donation,
        'requests': requests,
        'similar_donations': similar_donations,
        'user_profile': request.user.userprofile
    })

@login_required
@donor_required
def donation_edit(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.user != donation.donor:
        messages.error(request, 'You are not authorized to edit this donation.')
        return redirect('chat:donation_detail', pk=pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated successfully!')
            return redirect('chat:donation_detail', pk=pk)
    else:
        form = DonationForm(instance=donation)
    
    return render(request, 'chat/donation_form.html', {
        'form': form,
        'donation': donation,
        'user_profile': request.user.userprofile
    })

@login_required
@donor_required
def donation_delete(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.user != donation.donor:
        messages.error(request, 'You are not authorized to delete this donation.')
        return redirect('chat:donation_detail', pk=pk)
    
    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donation deleted successfully!')
        return redirect('chat:donation_list')
    
    return render(request, 'chat/donation_confirm_delete.html', {
        'donation': donation,
        'user_profile': request.user.userprofile
    })

@login_required
@recipient_required
def donation_request(request, pk):
    """Handle donation request and create initial chat message."""
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.user == donation.donor:
        messages.error(request, 'You cannot request your own donation.')
        return redirect('chat:donation_detail', pk=pk)
    
    if donation.status != 'AVAILABLE':
        messages.error(request, 'This donation is no longer available.')
        return redirect('chat:donation_detail', pk=pk)
    
    # Check if user already has a pending request
    existing_request = PickupRequest.objects.filter(
        donation=donation,
        recipient=request.user,
        status__in=['PENDING', 'SCHEDULED']
    ).first()
    
    if existing_request:
        messages.warning(request, "You already have a pending request for this donation.")
        return redirect('chat:chat_detail', user_id=donation.donor.id)
    
    if request.method == 'POST':
        try:
            pickup_date = request.POST.get('pickup_date')
            
            # Create pickup request
            pickup_request = PickupRequest.objects.create(
                donation=donation,
                recipient=request.user,
                pickup_date=pickup_date,
                status='PENDING'
            )
            
            # Update donation status
            donation.status = 'PENDING'
            donation.save()
            
            # Send initial message to donor
            initial_message = f"Hi! I'm interested in your donation: {donation.item_name}. I've requested a pickup for {pickup_date}."
            DirectMessage.objects.create(
                sender=request.user,
                recipient=donation.donor,
                content=initial_message
            )
            
            messages.success(request, "Request submitted successfully. You can now chat with the donor.")
            return redirect('chat:chat_detail', user_id=donation.donor.id)
            
        except Exception as e:
            messages.error(request, f"Error submitting request: {str(e)}")
            return redirect('chat:donation_detail', pk=pk)
    
    return render(request, 'chat/donation_request.html', {'donation': donation})

@login_required
@donor_required
def donation_mark_unavailable(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.user != donation.donor:
        messages.error(request, 'You are not authorized to mark this donation as unavailable.')
        return redirect('chat:donation_detail', pk=pk)
    
    if request.method == 'POST':
        donation.status = 'UNAVAILABLE'
        donation.save()
        messages.success(request, 'Donation marked as unavailable.')
        return redirect('chat:donation_detail', pk=pk)
    
    return redirect('chat:donation_detail', pk=pk)

@login_required
def request_pickup(request, pk):
    """Handle pickup request for a donation."""
    donation = get_object_or_404(Donation, pk=pk)
    
    # Check if user is not the donor
    if request.user == donation.donor:
        messages.error(request, "You cannot request pickup for your own donation.")
        return redirect('chat:donation_detail', pk=pk)
    
    # Check if donation is still available
    if donation.status != 'AVAILABLE':
        messages.error(request, "This donation is no longer available.")
        return redirect('chat:donation_detail', pk=pk)
    
    # Check if user already has a pending request
    existing_request = PickupRequest.objects.filter(
        donation=donation,
        recipient=request.user,
        status__in=['PENDING', 'SCHEDULED']
    ).first()
    
    if existing_request:
        messages.warning(request, "You already have a pending request for this donation.")
        return redirect('chat:donation_detail', pk=pk)
    
    if request.method == 'POST':
        try:
            pickup_date = request.POST.get('pickup_date')
            
            # Create pickup request
            pickup_request = PickupRequest.objects.create(
                donation=donation,
                recipient=request.user,
                pickup_date=pickup_date,
                status='PENDING'
            )
            
            # Create or get chat room for donor and recipient
            room_name = f'donation_{donation.pk}_{donation.donor.username}_{request.user.username}'
            room, created = Room.objects.get_or_create(
                name=room_name,
                defaults={
                    'donation': donation,
                    'donor': donation.donor,
                    'recipient': request.user
                }
            )
            
            messages.success(request, "Pickup request submitted successfully. You can now chat with the donor.")
            return redirect('chat:room', room_name=room.name)
            
        except Exception as e:
            messages.error(request, f"Error submitting pickup request: {str(e)}")
            return redirect('chat:donation_detail', pk=pk)
    
    return redirect('chat:donation_detail', pk=pk) 