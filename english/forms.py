from django import forms
from learn.models import Package
from django.contrib.auth.forms import PasswordChangeForm


class PurchaseForm(forms.Form):
    package = forms.ModelChoiceField(queryset=Package.objects.all(), empty_label=None, widget=forms.RadioSelect)
    card_number = forms.CharField(label='Card Number', max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Enter your card number'}))
    cvv = forms.CharField(label='CVV', max_length=4, widget=forms.TextInput(attrs={'placeholder': 'Enter CVV'}))
    exp_date = forms.CharField(label='Expiration Date', max_length=7, widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}))
    card_name = forms.CharField(label='Cardholder Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter cardholder name'}))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter current password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'





