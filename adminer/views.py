from django.shortcuts import render, redirect


def home(request):
    if 'admin' in request.session:
        content = {
            "client": 1
        }
        return render(request, 'adminer/index.html', content)
    else:
        return redirect('auth:auth')


def exit(request):
    if 'admin' in request.session:
        del request.session['token']
        del request.session['admin']
        return redirect('auth:auth')
    else:
        return redirect('auth:auth')
