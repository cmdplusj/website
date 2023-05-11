from django.urls import path, re_path

from soon import views as soon_views

urlpatterns = [
    path('', soon_views.soon_home, name='soon_home'),
]