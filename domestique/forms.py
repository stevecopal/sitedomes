
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
from domestique.models import Client, Provider, Admin, Service

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    email = forms.EmailField(label=_('Email'))
    phone = forms.CharField(label=_('Phone'))
    address = forms.CharField(widget=forms.Textarea, label=_('Address'))
    photo = forms.ImageField(label=_('Photo'), required=False)
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    password_confirm = forms.CharField(widget=forms.PasswordInput, label=_('Confirm Password'))
    role = forms.ChoiceField(choices=(('CLIENT', 'Client'), ('PROVIDER', 'Provider')), label=_('Role'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError(_('Passwords do not match'))
        return cleaned_data

    def save(self):
        role = self.cleaned_data['role']
        user_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
            'phone': self.cleaned_data['phone'],
            'address': self.cleaned_data['address'],
            'photo': self.cleaned_data.get('photo'),
            'role': role,
        }
        if role == 'CLIENT':
            user = Client.objects.create_user(password=self.cleaned_data['password'], **user_data)
        elif role == 'PROVIDER':
            user = Provider.objects.create_user(password=self.cleaned_data['password'], **user_data)
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label=_('Email'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))

class ServiceForm(TranslatableModelForm):
    class Meta:
        model = Service
        fields = ['category', 'notes']
        translated_fields = ['name', 'description']