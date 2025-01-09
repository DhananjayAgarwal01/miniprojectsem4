from django.db import models
from django.contrib.auth.models import User

# Chat Models
class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'

# Donation System Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[
        ('DONOR', 'Donor'),
        ('RECIPIENT', 'Recipient'),
        ('ORGANIZATION', 'Organization'),
        ('ADMIN', 'Admin'),
    ])
    profile_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.user_type}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Donation(models.Model):
    donor = models.ForeignKey(User, related_name='donations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_donations', null=True, blank=True, on_delete=models.SET_NULL)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=50, choices=[
        ('NEW', 'New'),
        ('EXCELLENT', 'Used - Excellent'),
        ('GOOD', 'Used - Good'),
        ('FAIR', 'Used - Fair'),
    ])
    donation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('AVAILABLE', 'Available'),
        ('PENDING', 'Pending Pickup'),
        ('PICKED_UP', 'Picked Up'),
        ('DELIVERED', 'Delivered'),
    ], default='AVAILABLE')
    image_path = models.ImageField(upload_to='donations/', null=True, blank=True)

    def __str__(self):
        return f'{self.item_name} by {self.donor.username}'

class PickupRequest(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='pickup_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')

    def __str__(self):
        return f'Request by {self.recipient.username} for {self.donation.item_name}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_chat_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_chat_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: {self.content[:50]}'
