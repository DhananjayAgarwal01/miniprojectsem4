from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
import json
from ..models import Donation, PickupRequest, Message
from ..decorators import donor_required

@login_required
def donation_filter(request):
    donations = Donation.objects.filter(status='AVAILABLE')
    
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    query = request.GET.get('q')
    
    if category:
        donations = donations.filter(category__name=category)
    if condition:
        donations = donations.filter(condition=condition)
    if query:
        donations = donations.filter(
            Q(item_name__icontains=query) |
            Q(description__icontains=query)
        )
    
    data = []
    for donation in donations:
        data.append({
            'id': donation.id,
            'item_name': donation.item_name,
            'description': donation.description,
            'category': donation.category.name,
            'condition': donation.condition,
            'image_url': donation.image_path.url if donation.image_path else None
        })
    
    return JsonResponse({'donations': data})

@login_required
@donor_required
@require_POST
def update_request_status(request):
    data = json.loads(request.body)
    request_id = data.get('request_id')
    new_status = data.get('status')
    
    pickup_request = get_object_or_404(PickupRequest, pk=request_id)
    donation = pickup_request.donation
    
    if request.user != donation.donor:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    old_status = pickup_request.status
    pickup_request.status = new_status
    pickup_request.save()
    
    if new_status == 'ACCEPTED' and old_status != 'ACCEPTED':
        # Send notification message to recipient
        notification_message = (
            f"Your request for '{donation.item_name}' has been accepted! "
            f"Please arrange pickup details with the donor. "
            f"Pickup date: {pickup_request.pickup_date.strftime('%B %d, %Y')}"
        )
        Message.objects.create(
            sender=request.user,
            recipient=pickup_request.recipient,
            content=notification_message
        )
        
        # Update donation status
        donation.status = 'PENDING'
        donation.save()
        
    elif new_status == 'COMPLETED':
        # Send completion message
        completion_message = f"Donation of '{donation.item_name}' has been marked as completed. Thank you for using our platform!"
        Message.objects.create(
            sender=request.user,
            recipient=pickup_request.recipient,
            content=completion_message
        )
        
        donation.status = 'DELIVERED'
        donation.recipient = pickup_request.recipient
        
    elif new_status == 'REJECTED':
        # Send rejection message
        rejection_message = f"Your request for '{donation.item_name}' has been declined. Please check other available donations."
        Message.objects.create(
            sender=request.user,
            recipient=pickup_request.recipient,
            content=rejection_message
        )
        
        donation.status = 'AVAILABLE'
        donation.recipient = None
    
    donation.save()
    
    return JsonResponse({'status': 'success'}) 