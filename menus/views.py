from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item
from .forms import  ItemForm
from django.http import HttpResponseRedirect,Http404
from django.contrib import messages
# Create your views here.

class ItemListView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        user = request.user
        is_following_users_id = [x.user.id for x in user.is_following.all()]
        user_items = Item.objects.filter(user=user)
        qs = Item.objects.filter(user__id__in=is_following_users_id)
        queryset = user_items | qs #merge querysets 
        all_items = queryset.distinct().order_by('-timestamp')
        return render(request, 'menus/menulist.html', {'object_list':all_items})

class ItemDetailView(DetailView):
    template_name = 'menus/menudetail.html'
    model = Item
    context_object_name = 'menu'
    # def get_queryset(self):
    #     return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin,CreateView):
    template_name = 'menus/create.html'
    form_class = ItemForm

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, 'Menu Item Uploaded')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Add Menu'
        return context

class ItemUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'menus/update.html'
    form_class = ItemForm

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Update Menu'
        return context
    
    def form_valid(self,form):
        instance = form.save()
        messages.warning(self.request, 'Menu Item Edited.')
        return HttpResponseRedirect(instance.get_absolute_url())


def ItemDeleteView(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.user:
        if request.method == 'POST':
            item.delete()
            messages.error(request, 'Menu Item \"{0}\" deleted'.format(item.name))
            return HttpResponseRedirect(request.user.userprofile.get_absolute_url())
        else:
            return HttpResponseRedirect(request.user.userprofile.get_absolute_url())
    return HttpResponseRedirect(request.user.userprofile.get_absolute_url())
    