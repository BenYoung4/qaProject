from django.contrib import admin
from django.urls import path, include

from dashboard.views import home_view

urlpatterns = [
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('tickets/', include('tickets.urls'))
]
