from django import forms
from .models import Item
from restaurant.models import RestaurantModel
class ItemForm(forms.ModelForm):   
    name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'name of menu item'}),
    )

    contents = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class':'form-control','placeholder':'contents of menu'}),
    ) 

    class Meta:
        model = Item
        fields = [
            'restaurant',
            'name',
            'contents',
            'image',
            'public',
        ]

        widgets = {
            'restaurant':forms.Select(attrs={'class':'form-control mb-2'}),
            #'name':forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'name of menu item'}),
           # 'contents':forms.Textarea(attrs={'class':'form-control','placeholder':'contents of menu'}),
            
        }
    
    def __init__(self,user=None,*args,**kwargs):
        super(ItemForm, self).__init__(*args,**kwargs)
        self.fields['restaurant'].queryset = RestaurantModel.objects.filter(owner=user)