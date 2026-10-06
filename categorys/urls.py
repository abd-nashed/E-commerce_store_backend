from django.urls import path
from . import views

urlpatterns = [
       path('add_category/',views.add_category,name='add_category'),
       path('get_categories/',views.get_categories,name='get_categories'),
       path('delete_category/<int:pk>/',views.delete_category,name='delete_category'),
       path('update_category/<int:pk>/',views.update_category,name='update_category'),
]