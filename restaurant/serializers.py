from rest_framework import serializers
from .models import RestaurantModel
from django.contrib.auth.models import User

class RestaurantSerializerModel(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RestaurantModel
        fields = ('id','url','name','location','category','timestamp')