from django.contrib import admin
from .models import Author, Comment, Post, Tag

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date", "image_name")
    list_filter = ("author", "tags", "date")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")
    list_filter = ['post']

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
