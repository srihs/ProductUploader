from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import userLoginForm

def login_view(request):
    next = request.GET.get('next')
    form = userLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(reverse('home'))
        context={'user':user}
        print(context)
        return redirect('home/',context)
    return render(request, 'authSection/login.html', {'form': form})


def logout_view(request):
    logout(request)
    form = userLoginForm()
    request.user.sessions.delete()
    return render (request,'authSection/login.html', {'form': form})
