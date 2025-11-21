from django.urls import path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.home, name='home'),
    path('summarize/', views.summarize_text, name='summarize'),
    path('api/summarize/', views.api_summarize, name='api_summarize'),
]