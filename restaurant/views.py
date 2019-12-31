from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from .models import RestaurantModel
from menus.models import Item
from django.db.models import Q
from django.views.generic import ListView,DetailView,CreateView,UpdateView,View,DeleteView
from .forms import RestaurantCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

class RestaurantListView(LoginRequiredMixin,View):    
    def get(self,request,*args,**kwargs):
        user = request.user
        is_following_users_id = [x.user.id for x in user.is_following.all()]
        user_items = RestaurantModel.objects.filter(owner=user)
        qs = RestaurantModel.objects.filter(owner__id__in=is_following_users_id)
        queryset = user_items | qs #merge querysets 
        all_items = queryset.distinct().order_by('-timestamp')
        return render(request, 'restaurant/restaurant_list.html', {'object_list':all_items})
 
def RestaurantDetailView(request,pk,slug):
    restaurant = get_object_or_404(RestaurantModel, pk=pk,slug=slug)
    restaurant_nearby = RestaurantModel.objects.filter(location = restaurant.location).exclude(pk=pk).order_by('?')[:3]

    fav = False
    if request.user.userprofile.favourites.filter(id=restaurant.id).exists():
        fav = True
    else:
        fav = False

    is_liked = False
    if restaurant.like.filter(id=request.user.id).exists():
        is_liked = True

    total_likes = restaurant.like.all()
    context = {
        'favrestaurants':request.user.userprofile.favourites.filter(id=restaurant.id),
        'fav':fav,
        'restaurant':restaurant,
        'nearby':restaurant_nearby,
        'is_liked':is_liked,
        'total_likes':total_likes,
    }
    return render(request, 'restaurant/restaurant_detail.html',context)

class SearchResultsView(LoginRequiredMixin,ListView):
    template_name = 'search.html'
    model = RestaurantModel
    def get_queryset(self):
        search_query = self.request.GET.get('q')
        object_list = RestaurantModel.objects.filter(
            Q(name__icontains = search_query) | 
            Q(location__icontains = search_query) |
            Q(category__icontains = search_query)
        )
        return object_list

    context_object_name = 'restaurants' # this is context name for the object_list

    def get_context_data(self,**kwargs):
        search_query = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        context['menu_items'] =  Item.objects.filter(
            Q(name__icontains=search_query) |
            Q(contents__icontains = search_query)
        )
        context['users'] = User.objects.filter(
            Q(username__icontains = search_query)
        )
        return context

class ExplorePage(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        restaurant_items = RestaurantModel.objects.all().order_by('?')
        menu_items       = Item.objects.filter(public=True).order_by('?')
        user             = request.user
        not_following_users = UserProfile.objects.all().exclude(Q(followers__id=user.id)|Q(user = user)).order_by('?')
    
        context = {
            'res':restaurant_items,
            'mes':menu_items,
            'users':not_following_users,
        }
        return render(request, 'explore.html', context)
        
class RestaurantCreateView(LoginRequiredMixin,CreateView):
    form_class = RestaurantCreateForm
    template_name = 'restaurant/create.html'
  
    
    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        messages.success(self.request, 'Restaurant Uploaded.')
        return HttpResponseRedirect(instance.get_absolute_url())
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Add Restaurant'
        return context

class RestaurantUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    template_name = 'restaurant/edit.html'
    form_class    = RestaurantCreateForm
    success_message = 'Restaurant successfully edited.'
    def get_context_data(self,*args,**kwargs):
        context = super(RestaurantUpdateView,self).get_context_data(*args,**kwargs)
        context['title'] = 'Edit Restaurant'
        return context

    def get_queryset(self):
        return RestaurantModel.objects.filter(owner=self.request.user) 

@login_required
def RestaurantDeleteView(request, pk, slug):
    restaurant = get_object_or_404(RestaurantModel, pk=pk, slug=slug)
    if request.user == restaurant.owner:
        if request.method == 'POST':
            restaurant.delete()
            messages.success(request, "Restaurant \"{0}\" deleted.".format(restaurant.name))
            return HttpResponseRedirect(request.user.userprofile.get_absolute_url())
    else:
        return HttpResponseRedirect(request.user.userprofile.get_absolute_url())

@login_required
def AddToDashboard(request, pk, slug):
    userprofile = request.user.userprofile
    restaurant = get_object_or_404(RestaurantModel, pk=pk, slug=slug)
    fav = False
    if userprofile.favourites.filter(id=restaurant.id).exists():
        userprofile.favourites.remove(restaurant)
        messages.error(request, '\"{0}\" removed from bookmarks'.format(restaurant.name))
        fav = True
    else:
        userprofile.favourites.add(restaurant)
        messages.success(request, '\"{0}\" added to bookmarks'.format(restaurant.name))
        fav = False
    context = {
        'favrestaurants':userprofile.favourites.filter(id=restaurant.id),
        'fav':fav,
    }
    return HttpResponseRedirect(restaurant.get_absolute_url())

def DashboardView(request):
    favRestaurants = request.user.userprofile.favourites.all()
    return render(request,'restaurant/dashboard.html',{'favrestaurants':favRestaurants})

@login_required
def RemoveFromDashboard(request):
    userprofile = request.user.userprofile
    restaurant = RestaurantModel.objects.get(id=request.POST.get('favrest'))
    userprofile.favourites.remove(restaurant)
    messages.error(request, '\"{0}\" removed from bookmarks'.format(restaurant.name))
    fav = False
    context = {
        'favrestaurants':userprofile.favourites.filter(id=restaurant.id),
        'fav':fav,
    }
    return HttpResponseRedirect(userprofile.get_absolute_url())

@login_required
def LikeRestaurant(request):
    restaurant = get_object_or_404(RestaurantModel, id=request.POST.get('res_id'))
    is_liked = False
    if restaurant.like.filter(id=request.user.id).exists():
        restaurant.like.remove(request.user)
        is_liked = False
    else:
        restaurant.like.add(request.user)
        is_liked = True
    
    return HttpResponseRedirect(restaurant.get_absolute_url())

    



    







