from django import forms


class AuthForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, label="Email")
    password = forms.CharField(max_length=100, required=True, label="Пароль", widget=forms.PasswordInput())