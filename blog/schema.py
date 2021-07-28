from typing import Text
from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from django.conf import settings
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_auth.decorators import login_required, verification_required
from .models import Tag, Article, Comment
from graphql_relay import from_global_id
from django_filters import FilterSet, CharFilter, OrderingFilter

"""Tag"""


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = {
            'name': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


class CreateTagMutation(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    tag = graphene.Field(TagNode)

    def mutate_and_get_payload(root, info, **input):
        tag = Tag(
            name=input.get('name'),
        )
        tag.save()
        return CreateTagMutation(tag=tag)


class UpdateTagMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    tag = graphene.Field(TagNode)

    def mutate_and_get_payload(root, info, **input):
        tag = Tag(
            id=from_global_id(input.get('id'))[1]

        )
        tag.name = input.get('name')
        tag.save()
        return UpdateTagMutation(tag=tag)


class DeleteTagMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    tag = graphene.Field(TagNode)

    def mutate_and_get_payload(root, info, **input):
        tag = Tag(
            id=from_global_id(input.get('id'))[1]

        )
        tag.delete()
        return DeleteTagMutation(tag=None)


"""Article"""


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = {
            "userArticle": ["exact"],
            "title": ['icontains'],
            "tags": ["exact"],
            "is_release": ["exact"],
            'created_at': ['lt', 'gt'],
            'updated_at': ['lt', 'gt'],
        }
    order_by_created_at = OrderingFilter(
        fields=(
            ('created_at'),
        )
    )
    order_by_updated_at = OrderingFilter(
        fields=(
            ('updated_at'),
        )
    )


class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article
        filterset_class = ArticleFilter
        interfaces = (relay.Node,)


class CreateArticleMutation(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        tags = graphene.List(graphene.ID)
        content = graphene.String(required=False)
        is_release = graphene.Boolean(required=True)
        liked = graphene.List(graphene.ID)

    article = graphene.Field(ArticleNode)

    def mutate_and_get_payload(root, info, **input):
        article = Article(
            userArticle=info.context.user.id,
            title=input.get('title'),
            content=input.get('content'),
            is_release=input.get('is_release'),
        )
        if input.get('tags') is not None:
            tags_set = []
            for tag in input.get('tags'):
                tag_id = from_global_id(tag)[1]
                tag_obj = Tag.objects.get(id=tag_id)
                tags_set.append(tag_obj)
            article.tags.set(tags_set)
        if input.get('liked') is not None:
            like_set = []
            for like in input.get('liked'):
                like_id = from_global_id(like)[1]
                like_obj = settings.AUTH_USER_MODEL.objects.get(id=like_id)
                like_set.append(like_obj)
            article.tags.set(like_set)

        article.save()
        return CreateArticleMutation(article=article)


class UpdateArticleMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        tags = graphene.List(graphene.ID)
        content = graphene.String(required=True)
        is_release = graphene.Boolean(required=True)
        liked = graphene.List(graphene.ID)

    article = graphene.Field(ArticleNode)

    def mutate_and_get_payload(root, info, **input):
        article = Article.objects.get(id=from_global_id(input.get('id'))[1])
        if input.get("title") is not None:
            article.title = input.get("title")
        if input.get('tags') is not None:
            tags_set = []
            for tag in input.get('tags'):
                tag_id = from_global_id(tag)[1]
                tag_obj = Tag.objects.get(id=tag_id)
                tags_set.append(tag_obj)
            article.tags.set(tags_set)
        if input.get("content") is not None:
            article.content = input.get("content")
        if input.get("is_release") is not None:
            article.is_release = input.get("is_release")
        if input.get('liked') is not None:
            like_set = []
            for like in input.get('liked'):
                like_id = from_global_id(like)[1]
                like_obj = settings.AUTH_USER_MODEL.objects.get(id=like_id)
                like_set.append(like_obj)
            article.tags.set(like_set)

        article.save()
        return UpdateArticleMutation(article=article)


class DeleteArticleMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    article = graphene.Field(ArticleNode)

    def mutate_and_get_payload(root, info, **input):
        article = Article(
            id=from_global_id(input.get('id'))[1]

        )
        article.delete()
        return DeleteArticleMutation(article=None)


"""Comment"""


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class CreateCommentMutation(relay.ClientIDMutation):
    class Input:
        text = graphene.String(required=True)
        articleComment = graphene.ID(required=True)

    comment = graphene.Field(CommentNode)

    def mutate_and_get_payload(root, info, **input):
        comment = Comment(
            text=input.get('text'),
            userComment=info.context.user.id,
            articleComment=input.get('articleComment'),
        )
        comment.save()
        return CreateCommentMutation(comment=comment)


class UpdateCommentMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        text = graphene.String(required=True)

    comment = graphene.Field(ArticleNode)

    def mutate_and_get_payload(root, info, **input):
        comment = Comment.objects.get(id=from_global_id(input.get('id'))[1])
        if input.get("text") is not None:
            comment.title = input.get("text")

        comment.save()
        return UpdateCommentMutation(comment=comment)


class DeleteCommentMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    comment = graphene.Field(ArticleNode)

    def mutate_and_get_payload(root, info, **input):
        comment = Comment(
            id=from_global_id(input.get('id'))[1]

        )
        comment.delete()
        return DeleteCommentMutation(comment=None)


"""---"""


class Mutation(graphene.AbstractType):
    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()
    create_article = CreateArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
    delete_article = DeleteArticleMutation.Field()
    create_comment = CreateCommentMutation.Field()
    update_comment = UpdateCommentMutation.Field()
    delete_comment = DeleteCommentMutation.Field()


class Query(graphene.ObjectType):
    all_tags = DjangoFilterConnectionField(TagNode)
    all_articles = DjangoFilterConnectionField(
        ArticleNode)
    all_comments = DjangoFilterConnectionField(CommentNode)

    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_all_articles(self, info, **kwargs):
        return Article.objects.all()

    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.all()
