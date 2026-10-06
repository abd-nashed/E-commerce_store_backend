# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('contact_protofolio/', views.contact_view, name='contact'),
]