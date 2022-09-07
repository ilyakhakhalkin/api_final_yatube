from sqlite3 import IntegrityError
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from posts.models import Post
from posts.models import Group
from .serializers import PostSerializer
from .serializers import GroupSerializer
from .serializers import CommentSerializer
from .serializers import FollowSerializer
from .permissions import IsAuthorOrReadonly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadonly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadonly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.followers.all()

    def perform_create(self, serializer):
        user = self.request.user

        if 'following' not in self.request.data.keys():
            raise ValidationError(
                'Отсутствует обязательное поле в теле запроса'
            )

        author = get_object_or_404(
            User,
            username=self.request.data['following']
        )
        if author == user:
            raise ValidationError(
                'Нельзя подписаться на самого себя'
            )
        try:
            serializer.save(user=user, following=author)
        except IntegrityError:
            raise ValidationError(
                'Пользователь уже подписан на этого автора'
            )
