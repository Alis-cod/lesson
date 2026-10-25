from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# =========================
# РЕГИСТРАЦИЯ
# =========================
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'})
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия'
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        # 👇 КЛЮЧЕВОЙ МОМЕНТ
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


# =========================
# РЕДАКТИРОВАНИЕ ПРОФИЛЯ
# =========================
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'specialization',
            'portfolio_url',
            'bio',
            'avatar'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Фамилия'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Специализация'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'https://example.com'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'О себе'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700'
            }),
        }
