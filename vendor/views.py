from django.shortcuts import render, get_object_or_404
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from vendor.models import Vendor
from .forms import VendorForm
# Create your views here.

def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor,
    }
    return render(request, 'vendor/vendor_profile.html', context)
