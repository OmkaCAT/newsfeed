import random
from .models import Post
from hashlib import sha256
from django.contrib import auth
from django.utils import timezone
from captcha.image import ImageCaptcha
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    post_list = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    page = 'index'
    return render(request, 'index.html', {'posts': posts, 'page': page})


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
        user = auth.authenticate(username=login, password=encrypt(password))
        if user is not None:
            auth.login(request, user)
            return redirect('/index')
        else:
            login_error = 'Некорректный логин или пароль!'
            context = {'login_error': login_error}
            return render(request, 'page_auth.html', context)
    else:
        return render(request, 'page_auth.html', context)


def page_register(request):
    context = {}
    if request.method == "POST":
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if User.objects.filter(username=login).count():
            login_error = 'Пользователь уже существует!'
            context = {'login_error': login_error}
            return render(request, 'page_register.html', context)
        User.objects.create_user(
            username=login,
            password=encrypt(password),
        )
        user = auth.authenticate(username=login, password=encrypt(password))
        if user is not None:
            auth.login(request, user)
        return redirect('/index')
    else:
        return render(request, 'page_register.html', {})


def page_profile(request, pk):
    posts = get_object_or_404(User, pk=pk)
    user = User.objects.get(pk=pk)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'page_profile.html', {'posts': posts, 'profile': user})


def add_post(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')
        Post.objects.create(
            title=title,
            text=text,
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
        print(text)
        update_post = Post.objects.get(pk=pk)
        Post.objects.select_related().filter(title=update_post).update(
            title=title,
            text=text,
            author=request.user
            )
        return redirect('/index')
    else:
        post = Post.objects.get(pk=pk)
        return render(request, 'edit_post.html', {'post': post})


def encrypt(string):
    signature = sha256(string.encode()).hexdigest()
    return signature
