from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from features.models import Post, Comment, Like, Follow
from features.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowSerializer,
)


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["author"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="author",
                description="Filter by author id",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request):
        """List posts with filter by author"""
        return super().list(request)


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["author"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="author",
                description="Filter by author id",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request):
        """List comments with filter by author"""
        return super().list(request)


class LikeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["user"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user", description="Filter by user id", required=False, type=str
            ),
        ]
    )
    def list(self, request):
        """List likes with filter by user"""
        return super().list(request)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["follower"]

    def create(self, request, *args, **kwargs):
        following = request.user
        followers = get_user_model().objects.get(id=request.data["follower"])
        if Follow.objects.filter(follower=following, followed=followers).exists():
            return Response(
                {"detail": "Already following"}, status=status.HTTP_400_BAD_REQUEST
            )
        follow = Follow.objects.create(follower=following, followed=followers)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="follower",
                description="Filter by follower id",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request):
        """List followed with filter by follower"""
        return super().list(request)
