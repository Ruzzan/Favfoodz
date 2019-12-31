from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile 
from django.contrib import auth
from django.http import Http404,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def SignupView(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username'])
                email = User.objects.get(email = request.POST['email'])
                return render(request, 'accounts/signup.html', {'error':'Username already taken.'})

            except User.DoesNotExist:
                avatar = request.FILES.get('avatar' or None)
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                prof = UserProfile.objects.create(user=user,avatar=avatar)
                prof.save()
                user.save()
                auth.login(request, user)
                messages.success(request, "You have been signed up. Login now.")
                return redirect('login')
        else:
            return render(request, 'accounts/signup.html', {'error':'Incorrect Passwords.'})
    else:  
        return render(request, 'accounts/signup.html')

def LoginView(request):
    if request.method == 'POST':
        user = auth.authenticate(username = request.POST['username'], password = request.POST['password'])

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'Welcome to FavFoodz ' + user.username)
                return redirect('explore')
        else:
            return render(request, 'accounts/login.html', {'error':'Invalid username or password.'})
    
    return render(request, 'accounts/login.html')

def LogoutView(request):
    auth.logout(request)
    messages.error(request, "You have been logged out.")
    return redirect('login')

def ProfileDetailView(request,username):
    user = User.objects.get(username=username) 
    requestedUser = request.user
    is_following = False
    dashboard_items = request.user.userprofile.favourites.all()
    if user.userprofile.followers.filter(id=requestedUser.id).exists():
        is_following = True
    context = {
        'user':user,
        'is_following':is_following,
        'followers':user.userprofile.followers.all(),
        'dashboard_items':dashboard_items,
    }
    return render(request,'accounts/detail.html',context)

def ProfileEditView(request, username):
    # user = User.objects.get(username=username)
    # if request.user == user:
    #     if request.method == 'POST':
    #         if request.POST.get('username') or request.POST.get('email') or request.POST.get('password1'):
    #             usernameNew = request.POST.get('username')
    #             passwordNew = request.POST.get('password1')
    #             emailNew    = request.POST.get('email')
    #             User.objects.filter(username=user.username).update(username=usernameNew,password = passwordNew,email= emailNew)
    # context = {'user':user}
    # return render(request, 'accounts/edit.html',context)
    pass
    
@login_required
def ProfileFollowToggle(request,user_profile_id):
    profile_to_follow = get_object_or_404(User, pk=user_profile_id)
    user_profile      = request.user
    is_following = False
    if request.method == "POST":
        if profile_to_follow.userprofile.followers.filter(id=user_profile.id).exists():
            is_following = False
            profile_to_follow.userprofile.followers.remove(user_profile)
            messages.warning(request, 'Unfollowed {0}'.format(profile_to_follow))
        else:
            profile_to_follow.userprofile.followers.add(user_profile)
            is_following = True
            messages.success(request, 'You started following {0}'.format(profile_to_follow))
    context = {
        'is_following': is_following,
        'followers': profile_to_follow.userprofile.followers.all()
    }
    return HttpResponseRedirect(profile_to_follow.userprofile.get_absolute_url())



        

    



