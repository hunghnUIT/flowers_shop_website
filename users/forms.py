from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',  'last_name', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

    class Meta: 
        # This class provide a nested namespace for configurations and 
        # keep those configurations in a place.
        # What we have in the "field" will have in model too.
        # And the model affected here is model User.
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone','image'] 


class CheckoutForm(forms.Form):
    receiver = forms.CharField(required=True)
    phone = forms.CharField(max_length=12, required=True)
    address = forms.CharField(max_length=70, required=True)


