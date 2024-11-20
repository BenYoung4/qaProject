from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from dashboard.views import home_view

urlpatterns = [
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('tickets/', include('tickets.urls')),

    # Add a redirect from the root URL to the login page
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True))
]
