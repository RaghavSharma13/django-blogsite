from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView, TemplateView
from django.urls import reverse

from blog.forms import CommentForm
from .models import Post
# Create your views here.

class IndexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.all().order_by("-date")[:3]
        context["posts"] = latest_posts
        return context
    


# def index(req):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(req, "blog/index.html", {
#         "posts": latest_posts
#     })

class PostListView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'My Collected Posts'
        return context
    


# def posts(req):
#     posts = Post.objects.all()
#     return render(req, "blog/all-posts.html", {
#         "posts": posts
#     })

class PostDetailView(View):
    model = Post
    template_name = "blog/post-detail.html"

    def is_stored_post(self, req, post_id):
        stored_posts = req.session.get('stored_posts')
        is_saved_for_later = (stored_posts is not None) and (post_id in stored_posts)
        return is_saved_for_later
    
    def get(self, req, slug):
        post = get_object_or_404(Post, slug=slug)
        context={
            "post": post,
            "tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
            "saved_for_later": self.is_stored_post(req, post.id)
        }
        return render(req, "blog/post-detail.html", context)

    def post(self, req, slug):
        post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(req.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        context={
            "post": post,
            "tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": comment_form,
            "saved_for_later": self.is_stored_post(req, post.id)
        }
        return render(req, "blog/post-detail.html", context)

# def post_detail(req, slug):
#     req_post = get_object_or_404(Post, slug=slug)
#     return render(req, "blog/post-detail.html", {
#         "post": req_post,
#         "tags": req_post.tags.all()
#     })

class ReadLaterView(View):
    def post(self, req):
        stored_posts = req.session.get('stored_posts')
        if stored_posts is None:
            stored_posts = []
        
        post_id = int(req.POST['post_id'])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        req.session['stored_posts'] = stored_posts
        return HttpResponseRedirect("/")
    def get(self, req):
        stored_posts = req.session.get('stored_posts')
        context={}
        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context['has_posts'] = False
            context['header'] = 'Stored Posts'
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True
            context['header'] = 'Stored Posts'
        return render(req, 'blog/stored-posts.html', context)
        