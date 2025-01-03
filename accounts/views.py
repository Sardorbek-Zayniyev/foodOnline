from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from accounts.utils import detect_user, check_role_vendor, check_role_customer, send_verification_email, create_user_and_send_verification_email, activate_user
from django.template.defaultfilters import slugify
from orders.models import Order
import datetime

# Create your views here.


def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('my_account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = create_user_and_send_verification_email(
                request, form, User.CUSTOMER, 'accounts/emails/account_verification_email.html')
            messages.success(
                request, "Your Email verification link has been successfully sent. Please click it to complete the verification process.")
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register_user.html', context)


def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('my_account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():

            user = create_user_and_send_verification_email(
                request, form, User.VENDOR, 'accounts/emails/account_verification_email.html')
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(
                request, "Your Email verification link has been successfully sent. Please click it to complete the verification process.")
            return redirect('login')
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/register_vendor.html', context)


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    user = activate_user(uidb64, token)
    if user is not None:
        messages.success(
            request, 'Congratulations! Your account is activated.')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
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
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/cust_dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return redirect('some_error_page')

    orders = Order.objects.filter(
        vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    recent_orders = orders[:10]

    # Current month's revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(
        vendors__in=[vendor.id], created_at__month=current_month)

    current_month_revenue = 0
    for order in current_month_orders:
        current_month_revenue += order.get_total_by_vendor(vendor)[
            'grand_total']

    # Total revenue
    total_revenue = 0
    grand_totals = []
    for order in orders:
        total_by_vendor = order.get_total_by_vendor(vendor)['grand_total']
        total_revenue += total_by_vendor
        grand_totals.append(total_by_vendor)

    orders_with_totals = zip(orders, grand_totals)

    context = {
        'orders_with_totals': orders_with_totals,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request, 'accounts/vendor_dashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(
                request, user, mail_subject, email_template)

            messages.success(
                request, 'Password reset link has been sent to your email address.')
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
