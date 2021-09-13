from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AuthForm


def auth(request):
    if 'admin' in request.session:
        return redirect('adminer:home')

    form = AuthForm()
    content = {
        'form': form
    }
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        if email == 'admin@gmail.com' and password == '11111':
            request.session['admin'] = 'admin'
            return redirect('adminer:polls')
        else:
            content['error'] = "Такого пользователя нет"

    return render(request, 'auth/auth.html', content)
