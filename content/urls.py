from django.urls import path
from . import views

urlpatterns = [
    # ⭐ للزوار — بدون توكن
    path('contact/', views.send_message, name='send_message'),

    # ⭐ للمسؤولين — مع توكن
    path('get_messages/', views.get_messages, name='get_messages'),
    path('delete_message/<int:pk>/', views.delete_message, name='delete_message'),
]