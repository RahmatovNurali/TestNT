from django.shortcuts import render, redirect

from accounts.forms import UsersCreationForm


# Create your views here.

def register(request):
    context = {
        'form': UsersCreationForm()
    }
    if request.method == 'POST':
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_page')
        context['form'] = form
    return render(request, 'auth/regester.html', context)
