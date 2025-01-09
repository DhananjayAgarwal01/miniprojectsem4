from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max, F, Count
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import DirectMessage

@login_required
def chat_list(request):
    """List of chat conversations."""
    # Get all users the current user has chatted with
    chat_users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()
    
    # Get the latest message and unread count for each conversation
    conversations = []
    for user in chat_users:
        latest_message = DirectMessage.objects.filter(
            Q(sender=request.user, recipient=user) |
            Q(sender=user, recipient=request.user)
        ).order_by('-timestamp').first()
        
        unread_count = DirectMessage.objects.filter(
            sender=user,
            recipient=request.user,
            is_read=False
        ).count()
        
        conversations.append({
            'user': user,
            'latest_message': latest_message,
            'unread_count': unread_count
        })
    
    # Sort conversations by latest message timestamp
    conversations.sort(key=lambda x: x['latest_message'].timestamp if x['latest_message'] else x['user'].date_joined, reverse=True)
    
    return render(request, 'chat/chat_list.html', {
        'conversations': conversations,
        'user_profile': request.user.userprofile
    })

@login_required
def chat_detail(request, user_id):
    """Individual chat conversation view."""
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        messages.error(request, "You cannot chat with yourself.")
        return redirect('chat:chat_list')
    
    # Mark all messages from other user as read
    DirectMessage.objects.filter(
        sender=other_user,
        recipient=request.user,
        is_read=False
    ).update(is_read=True)
    
    # Get conversation messages
    conversation = DirectMessage.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')
    
    return render(request, 'chat/chat_detail.html', {
        'other_user': other_user,
        'messages': conversation,
        'user_profile': request.user.userprofile
    })

@login_required
def send_message(request, user_id):
    """Send a message to another user."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    recipient = get_object_or_404(User, id=user_id)
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': 'Message content is required'}, status=400)
    
    if recipient == request.user:
        return JsonResponse({'error': 'You cannot send messages to yourself'}, status=400)
    
    try:
        message = DirectMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content
        )
        
        return JsonResponse({
            'id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%I:%M %p'),
            'sender': message.sender.username
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_unread_count(request):
    """Get the number of unread messages."""
    count = DirectMessage.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'unread_count': count}) 