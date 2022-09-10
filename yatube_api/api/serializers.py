from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Post
from posts.models import Group
from posts.models import Comment
from posts.models import Follow
from posts.models import User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        try:
            user = self.context.get('request').user
            following = self.context.get('request').data['following']
            author = User.objects.get(username=following)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Автор не найден'
            )
        except KeyError:
            raise serializers.ValidationError(
                'Отсутствует обязательное поле в запросе'
            )
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Follow.objects.filter(user=user, following=author).exists():
            raise serializers.ValidationError(
                'Пользователь уже подписан на этого автора'
            )

        return data
