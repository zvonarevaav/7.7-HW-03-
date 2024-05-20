from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


news = "NE"
articles = "AR"
POST_TYPES = [
    (news, "Новость"),
    (articles, "Статья")
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0)).get('cr')
        post_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'), 0)).get('pcr')

        print(posts_rating)
        print('-----------')
        print(comments_rating)
        print('-----------')
        print(post_comments_rating)

        self.rating = posts_rating * 3 + comments_rating + post_comments_rating
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
       return f"{self.text[:124]}..."



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()