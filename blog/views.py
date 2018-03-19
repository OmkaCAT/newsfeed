# -*- coding: utf8 -*-
import os
import json
from .models import Post, Captcha
from hashlib import sha256
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import choice
from string import ascii_uppercase
from captcha.image import ImageCaptcha


# Create your views here.
def index(request):
    post_list = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    ADD_PAGES = 2

    if posts.paginator.num_pages > ADD_PAGES * 2 + 1:
        start_window = posts.number - ADD_PAGES
        end_window = posts.number + ADD_PAGES

        if start_window < 1:
            start_window = 1
            end_window = 1 + ADD_PAGES * 2

        if end_window > posts.paginator.num_pages:
            end_window = posts.paginator.num_pages
            start_window = end_window - ADD_PAGES * 2

        my_page_range = range(start_window, end_window + 1)

    else:
        my_page_range = posts.paginator.page_range
    page = 'index'
    return render(request, 'index.html', {
        'posts': posts,
        'page': page,
        'my_page_range': my_page_range
        })


def root(request):
    return redirect('/index')


def logout(request):
    auth.logout(request)
    return redirect('/index')


def page_auth(request):
    context = {}
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('password')
        token = request.POST.get('captcha_token')
        captcha_user = request.POST.get('captcha_user')
        captcha_orig = Captcha.objects.get(token=token).captcha
        if login == '' or password == '':
            context = login_error('Введите пароль или логин!', token)
            return render(request, 'page_auth.html', context)
        elif captcha_user == '':
            context = login_error('Введите капчу!', token)
            return render(request, 'page_auth.html', context)
        elif captcha_orig == captcha_user:
            user = auth.authenticate(username=login, password=password)
            if user is not None:
                auth.login(request, user)
                delete_captcha(token)
                return redirect('/index')
            else:
                context = login_error('Неверное имя пользователя или пароль!', token)
                return render(request, 'page_auth.html', context)
        else:
            context = login_error('Капча введена неверно!', token)
            return render(request, 'page_auth.html', context)
    else:
        token = captcha()
        context = {'token': token}
        return render(request, 'page_auth.html', context)


def page_register(request):
    context = {}
    if request.method == "POST":
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')
        token = request.POST.get('captcha_token')
        captcha_user = request.POST.get('captcha_user')
        captcha_orig = Captcha.objects.get(token=token).captcha
        if login == '' or password == '':
            context = login_error('Введите пароль или логин!', token)
            return render(request, 'page_register.html', context)
        elif captcha_user == '':
            context = login_error('Введите капчу!', token)
            return render(request, 'page_register.html', context)
        elif captcha_orig == captcha_user:
            if User.objects.filter(username=login).count():
                context = login_error ('Пользователь уже существует!', token)
                return render(request, 'page_register.html', context)
            User.objects.create_user(
                username=login,
                password=password,
            )
            user = auth.authenticate(username=login, password=password)
            if user is not None:
                delete_captcha(token)
                auth.login(request, user)
            return redirect('/index')
        else:
            context = login_error('Капча введена неверно!', token)
            return render(request, 'page_register.html', context)
    else:
        token = captcha()
        context = {'token': token}
        return render(request, 'page_register.html', context)


def page_profile(request, pk):
    posts = get_object_or_404(User, pk=pk)
    user = User.objects.get(pk=pk)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    ADD_PAGES = 2

    if posts.paginator.num_pages > ADD_PAGES * 2 + 1:
        start_window = posts.number - ADD_PAGES
        end_window = posts.number + ADD_PAGES

        if start_window < 1:
            start_window = 1
            end_window = 1 + ADD_PAGES * 2

        if end_window > posts.paginator.num_pages:
            end_window = posts.paginator.num_pages
            start_window = end_window - ADD_PAGES * 2

        my_page_range = range(start_window, end_window + 1)

    else:
        my_page_range = posts.paginator.page_range
    return render(request, 'page_profile.html', {
        'posts': posts,
        'profile': user,
        'my_page_range': my_page_range
        })


def add_post(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')
        content_object = json.loads(text)
        Post.objects.create(
            title=title,
            text=content_object,
            author=request.user
        )
        return redirect('/index')
    else:
        page = 'add_post'
        return render(request, 'add_post.html', {'page': page})


def edit_post(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')
        update_post = Post.objects.get(pk=pk)
        Post.objects.select_related().filter(pk=pk).update(
            title=title,
            text=text,
            author=request.user
            )
        return redirect('/index')
    else:
        post = Post.objects.get(pk=pk)
        return render(request, 'edit_post.html', {'post': post})


def captcha():
    image = ImageCaptcha(fonts=['blog/fonts/A.ttf'])
    captcha = ''.join(choice(ascii_uppercase) for i in range(5))
    token = ''.join(choice(ascii_uppercase) for i in range(16))
    data = image.generate(captcha)
    path_token = 'blog/static/captchas/' + token + '.png'
    image.write(captcha, path_token)
    Captcha.objects.create(
        captcha=captcha,
        token=token,
    )
    return token


def delete_captcha(token):
    path_token = 'static/captchas/' + token + '.png'
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path_token)
    os.remove(path)
    Captcha.objects.filter(token=token).delete()


def login_error(error, token):
    delete_captcha(token)
    token = captcha()
    login_error = error
    context = {'login_error': login_error, 'token': token}
    return context

# def encrypt(string):
#     signature = sha256(string.encode()).hexdigest()
#     return signature
# текст
# heroku
# хеширование
