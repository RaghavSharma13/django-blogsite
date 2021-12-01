from django.core import validators
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.core.validators import MaxLengthValidator, MinLengthValidator

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption
    


class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.TextField(validators=[MaxLengthValidator(200)])
    image_name = models.ImageField(upload_to='article_images', height_field=None, width_field=None, max_length=None)
    
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])

    # one to many
    author = models.ForeignKey(to=Author,null= True, on_delete=SET_NULL, related_name="posts")
    # many to many
    tags = models.ManyToManyField(to=Tag)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")