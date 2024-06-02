from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from accounts.utils import detect_user, check_role_vendor, check_role_customer, send_verification_email, create_user_and_send_verification_email, activate_user


# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('my_account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = create_user_and_send_verification_email(request, form, User.CUSTOMER, 'accounts/emails/account_verification_email.html')
            messages.success(request, "Your Email verification link has been successfully sent. Please click it to complete the verification process.")
            return redirect('login')
    else:
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/register_user.html', context ) 

def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('my_account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
          
            user = create_user_and_send_verification_email(request, form, User.VENDOR, 'accounts/emails/account_verification_email.html')
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your Gmail verification link has been successfully sent. Please click it to complete the verification process.")
            return redirect('login')     
    else:
        form = UserForm()
        v_form = VendorForm()
    context ={
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/register_vendor.html', context)

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    user = activate_user(uidb64, token)
    if user:
        messages.success(request, 'Congratulations! Your account is activated.')
    else:
        messages.error(request, 'Invalid activation link')
    return redirect('my_account')

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
def my_account(request):
    user = request.user
    redirectUrl = detect_user(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cust_dashboard(request):
    return render(request, 'accounts/cust_dashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    user = activate_user(uidb64, token)
    if user:
        request.session['uid'] = user.pk
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('my_account')

def reset_password(request):
    
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')