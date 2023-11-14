from django.urls import path
from .views import home, profile, edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
