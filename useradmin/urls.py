from django.urls import path

from .views import dashboard

app_name = 'useradmin'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard')
]
