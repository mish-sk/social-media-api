from django.urls import path, include
from rest_framework import routers

from features.views import PostViewSet, CommentViewSet, LikeViewSet, FollowViewSet

router = routers.DefaultRouter()

router.register("post", PostViewSet)
router.register("comment", CommentViewSet)
router.register("like", LikeViewSet)
router.register("follow", FollowViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "features"
