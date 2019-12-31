from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from restaurant.apiview import RestaurantApiView

router = routers.DefaultRouter()
router.register('restaurant', RestaurantApiView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('restaurant.urls')),
    path('accounts/', include('accounts.urls')),
    path('menus/',include('menus.urls')),
    path('api/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
