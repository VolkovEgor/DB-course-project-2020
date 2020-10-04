from django import forms
from .my_models.collection import Collection
from .my_models.rating import RelativeRating
from .my_models.word import Word
from .my_models.user import User
from django.contrib.auth.forms import AuthenticationForm

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('title', 'level', 'is_public', 'image',)
    
    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username',)
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпали, попробуйте еще раз.')
        return cd['password2']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'photo',)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# class ChangeCollectionForm(forms.ModelForm):
#     class Meta:
#         model = Collection
#         fields = ('title', 'level', 'is_public', 'image')
    
#     def __init__(self, *argc, **kwargs):
#         super().__init__(*argc, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name',)

#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

# class ProfileEditMainForm(UserEditForm, ProfileEditForm):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
    # class Meta:
    #     model = User
    #     fields = ('username','password')
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user