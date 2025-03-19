from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    
    # Chat URLs
    path('messages/', views.chat_list, name='chat_list'),
    path('messages/<int:user_id>/', views.chat_detail, name='chat_detail'),
    path('messages/<int:user_id>/send/', views.send_message, name='send_message'),
    path('messages/unread/', views.get_unread_count, name='get_unread_count'),
    
    # Donation URLs
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/create/', views.donation_create, name='donation_create'),
    path('donations/<int:pk>/', views.donation_detail, name='donation_detail'),
    path('donations/<int:pk>/edit/', views.donation_edit, name='donation_edit'),
    path('donations/<int:pk>/delete/', views.donation_delete, name='donation_delete'),
    path('donations/<int:pk>/request/', views.donation_request, name='donation_request'),
    path('donations/<int:pk>/mark-unavailable/', views.donation_mark_unavailable, name='donation_mark_unavailable'),
    
    # API URLs
    path('api/donations/filter/', views.donation_filter, name='donation_filter'),
    path('api/requests/update-status/', views.update_request_status, name='update_request_status'),
]