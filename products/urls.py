from django.urls import path
from . import views

urlpatterns = [
    path('get_products/', views.get_products, name='get_products'),
    path('get_product/<int:pk>/', views.get_product, name='get_product'),
    path(
        'get_products_by_category/<int:category_id>/',
        views.get_products_by_category,
        name='get_products_by_category'
    ),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path(
    'get_products_by_store/<int:store_id>/',
    views.get_products_by_store,
    name='get_products_by_store'
),
]