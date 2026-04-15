from rest_framework import serializers
from .models import Post, Comment, Group, Follow
from django.contrib.auth.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author',)

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')

    def create(self, validated_data):
        request = self.context['request']
        view = self.context['view']
        

        post_id = view.kwargs.get('post_pk')
        
        if not post_id:
            raise serializers.ValidationError({"post": "Post ID is required."})
        
        
        from posts.models import Post
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError({"post": "Post does not exist."})
            
        validated_data['author'] = request.user
        validated_data['post'] = post_obj
        
        return super().create(validated_data)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("Нельзя подписаться на самого себя")

        if Follow.objects.filter(
            user=self.context['request'].user, 
            following=value).exists():
                raise serializers.ValidationError("Вы уже подписаны на этого пользователя")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
