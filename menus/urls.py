from django.urls import path
from .views import ItemListView,ItemDetailView,ItemCreateView,ItemUpdateView,ItemDeleteView
urlpatterns = [
    path('',ItemListView.as_view(),name='menu-list'),
    path('menu/<int:pk>',ItemDetailView.as_view(),name='menu-detail'),
    path('create/',ItemCreateView.as_view(),name='menu-create'),
    path('update/<int:pk>/',ItemUpdateView.as_view(),name='menu-update'),
    path('delete/<int:pk>/',ItemDeleteView,name='menu-delete'),
] 