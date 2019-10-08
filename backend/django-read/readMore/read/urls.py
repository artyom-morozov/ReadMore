from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="read-home"),
    path('about/', views.about, name="read-about"),
]
