"""
Forms module
"""
# pylint: disable=(too-few-public-methods, too-many-ancestors)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from . import models


class StyledUserCreationForm(UserCreationForm):
    """
    Create StyledUserCreationForm
    """

    class Meta:
        """
        Meta Class
        """
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите имя пользователя"
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите пароль"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Повторите пароль"
        })


class CustomUserAuthenticationForm(AuthenticationForm):
    """
    Create CustomUserAuthenticationForm
    """

    class Meta:
        """
        Meta Class
        """
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите имя пользователя"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": ""
        })


class UserProfileForm(forms.ModelForm):
    """
    Create UserProfileForm
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date"
            }
        )
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'})
    )
    repeat_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'})
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'})
    )

    class Meta:
        """
        Meta Class
        """
        model = models.UserProfile
        fields = ("first_name", "last_name", "email",
                  "phone", "date_of_birth", "avatar",
                  "newsletter_subscribed"
                  )

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["avatar"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["newsletter_subscribed"].widget.attrs.update({
            "class": "form-check-input",
        })

    def save(self, commit=True):
        """
        :param commit:
        :return:
        """
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if self.cleaned_data['password'] == self.cleaned_data['repeat_password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile.save()
        return profile


class CustomOrderForm(forms.ModelForm):
    """
    Create CustomOrderForm
    """
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email@email.com'})
    )
    phone = forms.CharField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': '0950000000'})
    )
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address'})
    )
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    postal_code = forms.CharField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    promo_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Promo Code'})
    )
    notes = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Notes'})
    )

    class Meta:
        """
        Meta Class
        """
        model = models.Order
        fields = (
            "first_name", "last_name", "email", "phone",
            "address", "city", "postal_code", "promo_code", "notes"
        )

    def save(self, commit=True):
        """
        :param commit:
        :return:
        """
        order = super().save(commit=False)
        order.delivery_method = "New post"
        order.payment_method = "Card payment"
        if commit:
            order.save()
        return order
