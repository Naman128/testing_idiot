from django.urls import path
from .views import (
    AddReviewView,
    SearchPlacesView,
    PlaceDetailView,
    UserReviewsView,
)

urlpatterns = [
    # Review endpoints
    path('reviews/', AddReviewView.as_view(), name='add-review'),
    path('reviews/my/', UserReviewsView.as_view(), name='my-reviews'),
    
    # Place endpoints
    path('places/search/', SearchPlacesView.as_view(), name='search-places'),
    path('places/<int:place_id>/', PlaceDetailView.as_view(), name='place-detail'),
]
