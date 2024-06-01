def detectUser(user):
    if user.is_superadmin:
        return '/admin'
    role_redirects = {
        1: 'vendor_dashboard',
        2: 'cust_dashboard',
    }
    return role_redirects.get(user.role, 'default_dashboard')