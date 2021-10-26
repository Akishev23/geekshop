from django import forms

from users.forms import UserRegisterForm, UserProfileForm

from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'image')


class UserAdminEditForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['image'].widget.attrs['readonly'] = False
