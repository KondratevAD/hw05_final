from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Group, Post, Follow


def index(request):
    """Возвращает главную страницу

        Ключевые аргументы:
        index.html -- имя HTML-шаблона главной страницы
        Post.object -- словарь с постами
        """
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, }
    )


def group_posts(request, slug):
    """Возвращает страницу сообщества

        Ключевые аргументы:
        group.html -- имя HTML-шаблона сообщества
        Post.object -- словарь с постами
        Group -- объект модели сообщества
        slug -- адрес страницы сообщества
        """
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).all()
    paginator = Paginator(post_list, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'page': page, 'group': group, },
    )


@login_required
def new_post(request):
    """Создает новый пост

        Ключевые аргументы:
        PostForm -- класс формы
        """
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    User = get_user_model()
    author = User.objects.get(username__iexact=username)
    post_list = Post.objects.filter(author=author).all()
    paginator = Paginator(post_list, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_post = page.paginator.count
    if request.user.username != username and request.user.is_authenticated:
        is_author = 'False'
        following = Follow.objects.filter(
            author=author,
            user=request.user
        ).exists()
    else:
        is_author = 'True'
        following = ''
    return render(request, 'profile/profile.html', {
        'author': author,
        'page': page,
        'all_post': all_post,
        'following': following,
        'is_author': is_author,
    })


def post_view(request, username, post_id):
    User = get_user_model()
    author = User.objects.get(username__iexact=username)
    post = Post.objects.get(id=post_id)
    all_post = Post.objects.filter(author=author).all().count
    form = CommentForm()
    return render(request, 'profile/post.html', {
        'post': post,
        'author': author,
        'all_post': all_post,
        'form': form,
    })


@login_required
def post_edit(request, username, post_id):
    editable_record = {
        'title': 'Редактирование поста',
        'header': 'Редактировать запись',
        'button': 'Сохранить запись',
    }
    post = Post.objects.get(id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.user != post.author:
        return redirect('index')
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post', username, post_id)
    return render(request, 'new.html', {
        'form': form,
        'post': post,
        'editable_record': editable_record
    })


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post_id = post_id
        comment.save()
    return redirect('post', username, post_id)


@login_required
def follow_index(request):
    author_list = set()
    for e in Follow.objects.filter(user=request.user).select_related('author'):
        author_list.add(e.author)
    post_list = Post.objects.filter(author__in=[i for i in author_list]).all()
    paginator = Paginator(post_list, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page, })


@login_required
def profile_follow(request, username):
    User = get_user_model()
    author = User.objects.get(username__iexact=username)
    if request.user.username != username:
        Follow.objects.get_or_create(
            author=author,
            user=request.user
        )
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    User = get_user_model()
    author = User.objects.get(username__iexact=username)
    if request.user != username:
        unfollow = Follow.objects.filter(
            author=author).filter(user=request.user)
        unfollow.delete()
        return redirect('profile', username)
    return redirect('index')
