from django.urls import path, re_path, include
from .views import BookDetailView, SearchResultsView, MyRatingsView
from . import views
urlpatterns = [
    re_path(r'^ratings/', include('star_ratings.urls', namespace="ratings")),
    path('', views.home, name="read-home"),
    path('book/<int:pk>/', BookDetailView.as_view(), name="book-detail"),
    path('about/', views.about, name="read-about"),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('my-ratings/', MyRatingsView.as_view(), name='my-ratings'),
    # path('add-rating/', views.add_rating, name='add-rating'),
]
