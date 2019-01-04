from django.urls import path 
from .views import ProfilesListView, ProfileDetailView

profiles_patterns =([
    path('', ProfilesListView.as_view(), name = 'profiles'),
    path('<username>/',ProfileDetailView.as_view(), name = 'profile_detail'),
],'profiles')