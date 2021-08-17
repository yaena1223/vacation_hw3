from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def showmain(request):
    return render(request, 'main/index.html')

def posts(request):
    posts = Post.objects.all()
    return render(request, 'main/posts.html', {'posts': posts})


def like(request):
    return render(request,'main/like.html')


def experience(request):
    return render(request,'main/experience.html')


def new(request):
    return render(request,'main/new.html')

def create(request):
    new_post= Post()
    new_post.title = request.POST['title']
    new_post.writer = request.user
    new_post.pub_date = timezone.now()
    new_post.image = request.FILES.get('image')
    new_post.body = request.POST['body']
    new_post.save()
    return redirect('main:detail', new_post.id)


def update(request, id): 
    update_post = Post.objects.get(id=id)
    update_post.title = request.POST['title']
    update_post.writer = request.user
    update_post.pub_date = timezone.now()
    update_post.image = request.FILES.get('image')
    update_post.body = request.POST['body']
    update_post.save()
    return redirect('main:detail', update_post.id)

def edit(request, id) : 
    edit_post = Post.objects.get(id=id)
    return render(request, 'main/edit.html',{'post':edit_post})

def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect('main:posts')



def detail(request,id):
    post = get_object_or_404(Post, pk =id)
    all_comments = post.comments.all().order_by('-created_at')
    post.view_count = post.view_count+1
    post.save()
    return render(request,'main/detail.html', {'post' : post,'comments':all_comments})

def create_comment(request,post_id):
    new_comment = Comment()
    new_comment.writer = request.user
    new_comment.content = request.POST['content']
    new_comment.post=get_object_or_404(Post,pk=post_id)
    new_comment.save()
    return redirect('main:detail',post_id)


def update_comment(request, comment_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method=="POST":
        comment.content = request.POST['content']
        comment.save()
        all_comments = post.comments.all()
        return redirect('main:detail', post.pk)
    return render(request, 'main/update_comment.html', {'comment' :comment})

def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('main:detail', post.pk)
    
@login_required
@require_POST

def like_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_like, post_like_created = Like.objects.get_or_create(user=request.user, post=post)

    if not post_like_created:
        post_like.delete()
        result = "like_cancel"
    else:
        result = "like"
    
    context = {
        "like_count":post.like_count,
        "result":result
    }

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@require_POST

def dislike_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_dislike, post_dislike_created = Dislike.objects.get_or_create(user=request.user, post=post)

    if not post_dislike_created:
        post_dislike.delete()
        result = "dislike_cancel"
    else:
        result = "dislike"
    
    context = {
        "dislike_count":post.dislike_count,
        "result":result
    }

    return HttpResponse(json.dumps(context), content_type="application/json")