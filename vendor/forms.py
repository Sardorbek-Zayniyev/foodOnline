from django import forms
from .models import Vendor, OpeningHour
from accounts.validators import allow_only_images_validator


class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license'] 
        
class OpeningHoursForm(forms.ModelForm):
    day = forms.ChoiceField(
        choices=[('', 'Select a day')] + list(OpeningHour._meta.get_field('day').choices),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    from_hour = forms.ChoiceField(
        choices=[('', 'From')] + list(OpeningHour._meta.get_field('from_hour').choices),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_hour = forms.ChoiceField(
        choices=[('', 'To')] + list(OpeningHour._meta.get_field('to_hour').choices),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
        