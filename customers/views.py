from django.shortcuts import render

# Create your views here.


def customer_profile (requset):
    return render(requset, 'customers/customer_profile.html')