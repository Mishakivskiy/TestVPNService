from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'user/', include("app.users.urls")),
    path(r'', include("app.product.urls")),
]
