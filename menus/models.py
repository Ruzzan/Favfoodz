from django.db import models
from django.contrib.auth.models import User
from restaurant.models import RestaurantModel
from django.urls import reverse
# Create your models here.

class Item(models.Model):
    #accosations
    user       = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantModel,on_delete=models.CASCADE)
    #item contents
    name       = models.CharField(max_length=100)
    contents   = models.TextField(help_text="Separate each by commas")
    image      = models.ImageField(upload_to='menus/%Y/%M/%d',blank=True,null=True)
    public     = models.BooleanField(default=True)
    timestamp  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_contents(self):
        return self.contents.split(',')

    def get_absolute_url(self):
        return  reverse('menu-detail',kwargs={'pk':self.id})

    class Meta:
        ordering = ['-timestamp'] 



