from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import User
# Create your models here.

class RestaurantModel(models.Model):
    owner     = models.ForeignKey(User, on_delete=models.CASCADE) #class_instance.modelname_set.all()
    name      = models.CharField(max_length=200)
    location  = models.CharField(max_length=200)
    category  = models.CharField(max_length=200)
    image     = models.ImageField(upload_to='images/%Y/%M/%d',blank=True,null=True)
    like      = models.ManyToManyField(User, related_name='likes', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug      = models.SlugField(unique=True,max_length=200,blank=True,null=True)

  

    def __str__(self):
        return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while RestaurantModel.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail", kwargs={'slug':self.slug, 'pk':self.id})

# using pre_save signal to caplitalize all the model fields before saving and displaying it 
def restaurant_pre_save(sender,instance,*args,**kwargs):
    instance.name = instance.name.capitalize()
    instance.location = instance.location.capitalize()
    instance.category = instance.category.capitalize()

pre_save.connect(restaurant_pre_save, sender=RestaurantModel)





        