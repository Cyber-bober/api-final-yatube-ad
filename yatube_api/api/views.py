from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow
from posts.serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from posts.permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post__pk=post_pk)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Для стандартных действий (list, retrieve) возвращаем подписки текущего пользователя
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Поиск подписок по имени пользователя.
        Используем ручную фильтрацию в Python для гарантированного точного совпадения,
        чтобы избежать проблем с SQL-фильтрами (icontains/startswith), которые могут
        находить лишних пользователей с похожими именами.
        """
        username = request.query_params.get('search')
        
        if not username:
            return Response({"error": "Параметр search обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Получаем все подписки текущего пользователя
        all_follows = Follow.objects.filter(user=request.user).select_related('following', 'user')
        
        # 2. Фильтруем вручную в Python по ТОЧНОМУ совпадению имени (регистронезависимо)
        # Это аналог iexact, но работает предсказуемо для тестовых данных
        filtered_follows = [
            follow for follow in all_follows 
            if follow.following.username.lower() == username.lower()
        ]
        
        # 3. Сериализуем результат
        serializer = self.get_serializer(filtered_follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
