import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def profile_picture_file_path(instance: "UserProfile", filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/profile_picture/", filename)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=profile_picture_file_path, blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
