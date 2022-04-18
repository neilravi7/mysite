from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout

# Create your views here.

def view_register(request):
    form = UserCreationForm(request.POST, None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/accounts/login')
    context = {"form": form}
    return render(request, "accounts/register.html", context)


# Login using in-built form
def view_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('article_list'))
        else:
            # print("error in user login")
            # return HttpResponse("Bad Request form is not valid")
            form = AuthenticationForm(request)
            context = {
                'form':form,
                'error':'invalid username password'
            }
            return render(request, 'accounts/login.html', context)
    else:
        form = AuthenticationForm(request)
        context = {'form':form}
        return render(request, 'accounts/login.html', context)


def view_logout(request):
    if request.method == 'POST':
        print("Calling Logout Function")
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'accounts/login.html', {})