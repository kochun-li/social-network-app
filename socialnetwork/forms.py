from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from socialnetwork.models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        # confirms that two fields matched to database
        user = authenticate(username=username, password=password)
        # if not found
        if not user:
            raise forms.ValidationError("Invalid username/password")
        
        return cleaned_data

class RegisterForm(forms.Form):
    username   = forms.CharField(max_length=20)
    password  = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    confirm_password  = forms.CharField(max_length=200, label='Confirm', widget=forms.PasswordInput())
    email      = forms.CharField(max_length=50, label='E-mail', widget=forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
    
    def clean_username(self):
        # Confirms that the username is not already present in the User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        
        return username

MAX_UPLOAD_SIZE = 2500000

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'id':'id_bio_input_text', 'rows':3}),
            'picture': forms.FileInput(attrs={'id':'id_profile_picture'})
        }
        labels = {
            'bio': "",
            'picture': "Upload image"
        }
    
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(f'File too big (max size is {MAX_UPLOAD_SIZE} bytes)')
        
        return picture
        
