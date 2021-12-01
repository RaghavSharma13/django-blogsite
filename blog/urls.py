from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name='index-page'),
    path("posts", views.PostListView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]
