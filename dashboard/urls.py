from django.urls import path
from . import views
from dashboard.views import home_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('', views.dashboard, name='dashboard')
]