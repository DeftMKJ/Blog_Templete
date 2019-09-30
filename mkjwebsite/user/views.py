from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm, NickNameForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Introduction


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
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            email = registerform.cleaned_data['email']
            password = registerform.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            user.save()

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

