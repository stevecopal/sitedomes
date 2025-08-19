
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
from domestique.models import Client, Provider, Admin, Service
from django.contrib.auth import authenticate

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        label=_('First Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Enter your first name')
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Enter your last name')
        })
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-input block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Enter your email')
        })
    )
    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Enter your phone number')
        })
    )
    address = forms.CharField(
        label=_('Address'),
        widget=forms.Textarea(attrs={
            'class': 'form-textarea block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Enter your address'),
            'rows': 3
        })
    )
    photo = forms.ImageField(
        label=_('Photo'),
        required=False
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Enter your password')
        })
    )
    password_confirm = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]',
            'placeholder': _('Confirm your password')
        })
    )
    role = forms.ChoiceField(
        label=_('Role'),
        choices=(('CLIENT', _('Client')), ('PROVIDER', _('Provider'))),
        widget=forms.Select(attrs={
            'class': 'form-select block w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2E8B57] focus:border-[#2E8B57]'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', _('Passwords do not match'))

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
            user = Client.objects.create_user(
                password=self.cleaned_data['password'],
                **user_data
            )
        elif role == 'PROVIDER':
            user = Provider.objects.create_user(
                password=self.cleaned_data['password'],
                **user_data
            )
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email"),
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#2E8B57]',
            'placeholder': _('Enter your email')
        })
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#2E8B57]',
            'placeholder': _('Enter your password')
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError(_("Invalid email or password"), code='invalid_login')

        return super().clean()


class ServiceForm(TranslatableModelForm):
    class Meta:
        model = Service
        fields = ['category', 'notes']
        translated_fields = ['name', 'description']