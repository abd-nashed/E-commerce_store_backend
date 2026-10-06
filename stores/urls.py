from django.urls import path
from . import views

urlpatterns = [
    # ============ المتاجر ============
    path('get_stores/', views.get_stores, name='get_stores'),
    path('get_store/<int:pk>/', views.get_store, name='get_store'),
    path('add_store/', views.add_store, name='add_store'),
    path('update_store/<int:pk>/', views.update_store, name='update_store'),
    path('delete_store/<int:pk>/', views.delete_store, name='delete_store'),

    # ============ طلبات المتاجر ============
    path('get_store_requests/', views.get_store_requests, name='get_store_requests'),
    path('send_store_request/', views.send_store_request, name='send_store_request'),
    path('approve_store_request/<int:pk>/', views.approve_store_request, name='approve_store_request'),
    path('reject_store_request/<int:pk>/', views.reject_store_request, name='reject_store_request'),
]