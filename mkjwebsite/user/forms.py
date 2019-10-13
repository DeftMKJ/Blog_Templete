from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Introduction


# forms.ModelForm 与 forms.Form
# 前者需要写入数据库，进行数据迁移  后者 如果提交表单后 不会对数据库就行修改，则继承Form类。
class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名或邮箱',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )

    # hook isvalid方法后续的验证
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'})
    )

    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )

    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入验证码'}
        )
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )

    password_again = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('register_send_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code', '').strip()
        if code == '':
            raise forms.ValidationError('验证码不能为空~')
        return code

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again


class NickNameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'})
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(NickNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')

    def clean_nickname_new(self):
        nickname = self.cleaned_data.get('nickname_new', '').strip()
        if nickname == '':
            raise forms.ValidationError('新的昵称不能为空')

        if Introduction.objects.filter(nick_name=nickname).exists():
            raise forms.ValidationError('昵称已被使用')
        return nickname


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}
        )
    )

    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入验证码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录~')

        if self.request.user.email:
            raise forms.ValidationError('用户已绑定邮箱~')

        code = self.request.session.get('bind_email_send_code', '')
        input_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == input_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被绑定~')
        return email

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code', '').strip()
        if code == '':
            raise forms.ValidationError('验证码不能为空~')
        return code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'})
    )
    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新的密码'})
    )
    new_password_again = forms.CharField(
        label='再次输入密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 新密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '' or new_password_again == '':
            raise forms.ValidationError('两次密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码验证错误')
        return old_password



class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱'}
        )
    )

    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入验证码'}
        )
    )

    new_password = forms.CharField(
        label='新的的密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新的密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email =  self.cleaned_data.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱下的用户不存在')
        return email


    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code', '').strip()
        if code == '':
            raise forms.ValidationError('验证码不能为空~')

        code = self.request.session.get('forget_password_send_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return code


