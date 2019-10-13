import re
import random
import string
import time
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from .forms import LoginForm, RegisterForm, NickNameForm, BindEmailForm, ChangePasswordForm, ForgetPasswordForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Introduction


def ErrorResponse(code, message):
    res = {}
    res['code'] = '%s' % code
    res['message'] = message
    res['status'] = 'ERROR'
    return JsonResponse(res)


def SuccessResponse():
    res = {}
    res['status'] = 'SUCCESS'
    res['code'] = '200'
    return JsonResponse(res)


def login_modal(request):
    loginForm = LoginForm(request.POST)
    res = {}
    if loginForm.is_valid():
        user = loginForm.cleaned_data['user']
        auth.login(request, user)
        res['code'] = '200'
    else:
        res['code'] = '10008'
    return JsonResponse(res)


def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = loginForm.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        loginForm = LoginForm()
    context = {}
    context['loginform'] = loginForm
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def register(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST, request=request)
        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            email = registerform.cleaned_data['email']
            password = registerform.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            user.save()

            del request.session['register_send_code']

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            return redirect(request.GET.get('from', reverse('home')))
    else:
        registerform = RegisterForm()
    context = {}
    context['registerform'] = registerform
    return render(request, 'user/register.html', context)


def user_info(request):
    return render(request, 'user/user_info.html', {})


def change_nick_name(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = NickNameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname = form.cleaned_data['nickname_new']
            instroduction, created = Introduction.objects.get_or_create(user=request.user)
            instroduction.nick_name = nickname
            instroduction.save()
            return redirect(redirect_to)
    else:
        form = NickNameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '提交'
    context['retern_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_send_code']
            return redirect(redirect_to)
            # TODO 输入错误
            # return ErrorResponse('500', list(form.errors.values())[0][0])
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['retern_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'user/bind_email.html', context)


def send_email_code(request):
    email = request.GET.get('email', '')
    send_type = request.GET.get('send_type', '')
    if email == '':
        return ErrorResponse('10006', '绑定邮箱为空')
    if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return ErrorResponse('10007', '绑定邮箱格式验证失败')

    if send_type != 'forget_password_send_code':
        if User.objects.filter(email=email).exists():
            return ErrorResponse('10009', '邮箱已被绑定~')

    code = ''.join(random.sample(string.digits + string.ascii_letters, 4))

    now = int(time.time())
    send_time = request.session.get('send_code_time', 0)
    if now - send_time < 30:
        return ErrorResponse('10008', '验证码发送太频繁')
    else:
        request.session['send_code_time'] = now
        request.session[send_type] = code

        send_mail(
            '绑定邮箱',
            '验证码：%s' % code,
            '714831204@qq.com',
            [email],
            fail_silently=False,
        )
        return SuccessResponse()


def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['retern_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'form.html', context)

def forget_password(request):
    redirect_to = reverse('user:login')
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST, request=request)
        if form.is_valid():
            # TODO 这里表单已经验证过了，因此直接拿肯定有值，比如【】，比如get不需要再判断
            new_password = form.cleaned_data['new_password']
            email =  form.cleaned_data['email']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['forget_password_send_code']
            return redirect(redirect_to)
    else:
        form = ForgetPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['retern_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'user/forget_password.html', context)
