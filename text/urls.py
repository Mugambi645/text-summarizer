from django.urls import path,include
from . import views

from .api.api_views import summarize_api, api_status

app_name = 'text'




# API URLs
api_patterns = [
    path('summarize/', summarize_api, name='api_summarize'),
    path('status/', api_status, name='api_status'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('summarize/', views.summarize_text, name='summarize'),
    path('api/summarize/', views.api_summarize, name='api_summarize'),
      
    # API URLs
    path('api/v1/', include(api_patterns)),
]