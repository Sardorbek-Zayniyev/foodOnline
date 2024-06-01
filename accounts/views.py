from django.shortcuts import render, redirect

from accounts.utils import detectUser, check_role_vendor, check_role_customer
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.



def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('my_account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            
            # Create user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name, username=username,email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your accounts has been registered successfully!")
            return redirect('login')
        # else:
        #     print(form.errors)
    else:
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/register_user.html', context ) 

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('my_account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']   
            user = User.objects.create_user(first_name=first_name,last_name=last_name, username=username,email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Your account has been registered successfully! Please wait for the approval.')
            return redirect('login')
        else:
            print(form.errors)
            
    else:
        form = UserForm()
        v_form = VendorForm()
    context ={
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/register_vendor.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('my_account')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect('my_account')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')
    

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/cust_dashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')
