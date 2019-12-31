from django.urls import path
from .views import SignupView, LoginView, LogoutView,ProfileDetailView,ProfileFollowToggle,ProfileEditView

urlpatterns = [
    path('signup/',SignupView,name='signup'),
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('<username>/',ProfileDetailView,name='profile-detail'),
    path('<username>/edit',ProfileEditView,name='edit-profile'),
    path('follow/<int:user_profile_id>/',ProfileFollowToggle,name='follow'),
] 