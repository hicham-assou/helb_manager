from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.

#creation de la register view
#creer un formulaire pout l'inscription
def register(request):

    if request.method == 'POST': #cas d'un envoi d'un formulaire

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, you can log in now !')
            return redirect('login')#une fois son compte cree, on le dirige vers la page de connexion
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})
@login_required
def profile(request):
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if update_form.is_valid() and profile_form.is_valid():
            update_form.save()
            profile_form.save()
            messages.success(request, f'Account updated')
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'update_form': update_form,
        'profile_form': profile_form
    }
    return render(request,'users/profile.html', context)