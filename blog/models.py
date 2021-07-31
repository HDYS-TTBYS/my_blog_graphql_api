from django.db import models
from django.contrib.auth import get_user_model


class Tag(models.Model):
    """タグモデル"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    """記事モデル"""
    user_article = models.ForeignKey(
        get_user_model(), related_name='user_article',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='tag', blank=True)
    content = models.TextField(blank=True, null=True)
    is_release = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    liked = models.ManyToManyField(
        get_user_model(), related_name='liked', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """コメントモデル"""
    text = models.TextField(blank=True, null=True)
    user_comment = models.ForeignKey(
        get_user_model(), related_name='user_comment',
        on_delete=models.CASCADE
    )
    article_comment = models.ForeignKey(
        Article, related_name='article_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.text
