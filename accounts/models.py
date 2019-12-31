from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from restaurant.models import RestaurantModel
# Create your models here.
class UserProfile(models.Model):
    user   = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/',blank=True,null=True)
    followers = models.ManyToManyField(User, related_name='is_following',blank=True,null=True)
    favourites = models.ManyToManyField(RestaurantModel,related_name='favourites',blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('profile-detail',kwargs={'username':self.user.username})