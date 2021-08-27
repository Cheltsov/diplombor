from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AuthForm


# Create your views here.
def auth(request):
    form = AuthForm()
    content = {
        'form': form
    }
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        if email=='admin@gmail.com' and password=='11111':
            request.session['token'] = 'admin'
            request.session['admin'] = 'admin'
            return redirect('adminer:home')
        else:
            content['error'] = "Такого пользователя нет"

    return render(request, 'auth/auth.html', content)
