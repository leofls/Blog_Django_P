from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post, Tag

def home(request):
    return render(request, 'core/home.html')

def blog_view(request, tag_id=None):
    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)
        posts = Post.objects.filter(tags=tag)
    else:
        posts = Post.objects.all()
        tag = None
    tags = Tag.objects.all()
    return render(request, 'core/blog.html', {'posts': posts, 'tags': tags, 'selected_tag': tag})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    tags = Tag.objects.all()
    return render(request, 'core/post_detail.html', {'post': post, 'tags': tags})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.save()
            
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'core/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.save()
            
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_edit.html', {'form': form})