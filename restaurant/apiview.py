from rest_framework import viewsets, permissions
from .models import RestaurantModel
from .serializers import RestaurantSerializerModel

class RestaurantApiView(viewsets.ModelViewSet):
    queryset = RestaurantModel.objects.all()
    serializer_class = RestaurantSerializerModel
    