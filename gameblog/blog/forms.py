from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa Użytkownika",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło",widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label="E-Mail",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Nazwa Użytkownika",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Hasło",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Powtórz hasło",widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    field_order = ['username', 'email', 'password1', 'password2']

class PostForm(forms.Form):
    content = forms.CharField(label="Zawartość",widget=forms.Textarea(attrs={'class': 'form-control'}))
    rating = forms.IntegerField(label="Ocena",widget=forms.NumberInput(attrs={'class': 'form-control'}))

class GameForm(forms.Form):
    title = forms.CharField(label="Tytuł",widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Opis",widget=forms.Textarea(attrs={'class': 'form-control'}))
    release_date = forms.DateField(label="Data wydania",widget=forms.DateInput(attrs={'class': 'form-control'}))
    developer = forms.CharField(label="Deweloper",widget=forms.TextInput(attrs={'class': 'form-control'}))
    publisher = forms.CharField(label="Wydawca",widget=forms.TextInput(attrs={'class': 'form-control'}))
    cover = forms.ImageField(label="Okładka",widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

class GenreForm(forms.Form):
    name = forms.CharField(label="Nazwa",widget=forms.TextInput(attrs={'class': 'form-control'}))