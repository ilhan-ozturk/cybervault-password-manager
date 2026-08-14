from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Credential
from .security import analyze_password

class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta: model=User; fields=('username','email','password1','password2')
    def clean_email(self):
        email=self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('This email is already registered.')
        return email

class CredentialForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'new-password','data-password-input':'1'}),min_length=8)
    notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':4,'placeholder':'Optional encrypted notes'}))
    class Meta:
        model=Credential; fields=('title','website','username','password','category','favorite','notes')
        widgets={'title':forms.TextInput(attrs={'placeholder':'e.g. GitHub'}),'website':forms.URLInput(attrs={'placeholder':'https://example.com'}),'username':forms.TextInput(attrs={'autocomplete':'off','placeholder':'email or username'})}
    def clean_password(self):
        value=self.cleaned_data['password']; result=analyze_password(value)
        if result['score']<25: raise forms.ValidationError('Password is critically weak. Use a longer, less predictable password.')
        return value
