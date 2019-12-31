from django.urls import path
from .views import (RestaurantListView,
RestaurantDetailView,
RestaurantCreateView,
RestaurantUpdateView,
RestaurantDeleteView,
SearchResultsView,
AddToDashboard,
RemoveFromDashboard,
LikeRestaurant,
ExplorePage,
)
urlpatterns = [
    path('',RestaurantListView.as_view(),name="home"),
    path('restaurant/<int:pk>/<slug:slug>/',RestaurantDetailView,name="detail"),
    path('explore/',ExplorePage.as_view(),name='explore'),
    path('search/',SearchResultsView.as_view(),name="search"),
    path('restaurant/create/',RestaurantCreateView.as_view(),name="create"),
    path('restaurant/edit/<int:pk>/<slug:slug>/',RestaurantUpdateView.as_view(),name="edit"),
    path('restaurant/add/<int:pk>/<slug:slug>/',AddToDashboard,name='add-dashboard'),
    path('restaurant/delete/<int:pk>/<slug:slug>/',RestaurantDeleteView,name="delete"),
    path('restaurant/remove/',RemoveFromDashboard,name='remove-dashboard'),
    path('like/',LikeRestaurant,name='like'),
]
