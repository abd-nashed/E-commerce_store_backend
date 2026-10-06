from django.urls import path
from . import views

urlpatterns = [
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('get_users/', views.get_users, name='get_users'),
    path('verify-superadmin/', views.verify_superadmin, name='verify_superadmin'),
    path('verify-me/', views.verify_me, name='verify_me'),   # ⭐ جديد
]