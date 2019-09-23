from django import forms
from django.contrib import auth


# forms.ModelForm 与 forms.Form
# 前者需要写入数据库，进行数据迁移  后者 如果提交表单后 不会对数据库就行修改，则继承Form类。
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

    # hook isvalid方法后续的验证
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名密码阿不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
