from django.core.exceptions import PermissionDenied

def detectUser(user):
    if user.is_superadmin:
        return '/admin'
    role_redirects = {
        1: 'vendor_dashboard',
        2: 'cust_dashboard',
    }
    return role_redirects.get(user.role, 'default_dashboard')

#restrictions
def check_role(user, required_role):
    if user.role != required_role:
        raise PermissionDenied
    return True

def check_role_vendor(user): 
    return check_role(user, 1)

def check_role_customer(user):
    return check_role(user, 2)