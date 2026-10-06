from django.urls import path
from . import views

urlpatterns = [
    # ⭐ للزوار
    path('create_order/', views.create_order, name='create_order'),
    path('track_order/<str:code>/', views.track_order, name='track_order'),

    # ⭐ للمسؤولين
    path('get_orders/', views.get_orders, name='get_orders'),
    path('get_order/<int:pk>/', views.get_order, name='get_order'),
    path('update_order_status/<int:pk>/', views.update_order_status, name='update_order_status'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('delete_all_orders/', views.delete_all_orders, name='delete_all_orders'),
    path('daily_sales/', views.get_daily_sales, name='daily_sales'),
]