from django import forms
from .models import RestaurantModel
from django.core.exceptions import ValidationError
class RestaurantCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Restaurant Name'}),label=''
    )
    location = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Restaurant Location'}),label=''
    )
    category = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Category'}),label=''
    )
    class Meta:
        model = RestaurantModel
        fields = ['name', 'location', 'category', 'image']
        # widgets = {
        #    # 'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Restaurant Name'}),
        #     'location':forms.TextInput(attrs={'class':'form-control','placeholder':'Location'}),
        #     'category':forms.TextInput(attrs={'class':'form-control','placeholder':'Category'}),
        # }

        