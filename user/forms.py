from django import forms
from django.contrib.auth.models import User
import re
from user.models import UserPro

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ('username','email')
    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get(('password2'))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        if not re.match('^[a-zA-Z0-9]+@[a-zA-Z0-9]+(\.[a-z]{2,4}){1,2}$', email):
            raise forms.ValidationError('邮箱格式不正确')
        if password != password2:
            raise forms.ValidationError('密码输入不一致')
        return cleaned_data

class UserProForm(forms.ModelForm):
    class Meta:
        model = UserPro
        fields = ('phone','avatar','bio')