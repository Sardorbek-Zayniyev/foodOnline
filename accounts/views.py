from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            return redirect('register_user')
    else:
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/register_user.html', context ) 