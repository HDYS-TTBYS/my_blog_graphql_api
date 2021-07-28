from django.db import models
from django.conf import settings


class Tag(models.Model):
    """タグモデル"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    """記事モデル"""
    userArticle = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userArticle', on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='tag', blank=True)
    content = models.TextField(blank=True, null=True)
    is_release = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """コメントモデル"""
    text = models.TextField(blank=True, null=True)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    articleComment = models.ForeignKey(
        Article, related_name='articleComment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.text
