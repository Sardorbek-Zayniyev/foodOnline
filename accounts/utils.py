from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from .models import User, UserProfile

def detect_user(user):
    """
    Detect the user type and return the corresponding redirect URL.
    """
    if user.is_superadmin:
        return '/admin'
    role_redirects = {
        1: 'vendor_dashboard',
        2: 'cust_dashboard',
    }
    return role_redirects.get(user.role, 'default_dashboard')

def check_role(user, required_role):
    """
    Check if the user's role matches the required role.
    """
    if user.role != required_role:
        raise PermissionDenied
    return True

def check_role_vendor(user):
    return check_role(user, 1)

def check_role_customer(user):
    return check_role(user, 2)

def send_notification(email_subject, email_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(email_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(email_subject, message, from_email, to=to_email)
    mail.send()
    
def send_verification_email(request, user, mail_subject, email_template):
    """
    Send a verification email to the user.
    """
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(email_template, context)
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send()
    
def create_user_and_send_verification_email(request, form, role, email_template):
    """
    Create a user with the given role and send a verification email.
    """
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    user.role = role
    user.save()
    mail_subject = 'Please activate your account'
    send_verification_email(request, user, mail_subject, email_template)
    return user

def activate_user(uidb64, token):
    """
    Activate the user by decoding the uidb64 and token.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return user
    return None