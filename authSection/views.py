from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from django import forms
from django.contrib import messages
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
        #when the 'next' parameter is not defined in the GET, it will be an empty string,
        #so this line will redirect to the next if defined or to home if not.
        return HttpResponseRedirect(request.POST.get('next') or reverse('mainSection:home'))
        context={'user':user}
        print(context)
        return redirect('home/',context)
    else:
        messages.error(request, form.errors)

    return render(request, 'authSection/login.html', {'form': form})


def logout_view(request):
    logout(request)
    form = userLoginForm()
    request.session.flush()
    return render (request,'authSection/login.html', {'form': form})
