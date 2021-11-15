from django import forms

from products.models import Category
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


class CategoryUpdateFormAdmin(forms.ModelForm):
    discount = forms.IntegerField(widget=forms.NumberInput(), label='Скидка', required=False,
                                  min_value=0, max_value=90,
                                  initial=0)

    class Meta:
        model = Category
        fields = ("title", "image", 'discount')

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateFormAdmin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
