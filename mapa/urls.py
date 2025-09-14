from django.urls import path
from django.views.generic import TemplateView
from .views import map_view

urlpatterns = [
    path('map/', map_view, name='map'),
    path('about/', TemplateView.as_view(template_name='mapa/about.html'), name='about'),
]