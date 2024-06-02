from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
    if user.is_superadmin:
        return '/admin'
    role_redirects = {
        1: 'vendor_dashboard',
        2: 'cust_dashboard',
    }
    return role_redirects.get(user.role, 'default_dashboard')

#restrict the user to access unauthorized pages"
def check_role(user, required_role):
    if user.role != required_role:
        raise PermissionDenied
    return True

def check_role_vendor(user): 
    return check_role(user, 1)

def check_role_customer(user):
    return check_role(user, 2)

#send verification email

def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()