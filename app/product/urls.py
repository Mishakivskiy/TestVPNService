from django.urls import path
from .views import home, profile, edit_profile, add_site, test, proxy_site
urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('add_site/', add_site, name='add_site'),
    path('test/', test, name='test'),
    path("<str:user_site_name>/<path:site_url>/", proxy_site, name="proxy_site"),
]
