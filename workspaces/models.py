from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import BaseModel


User = get_user_model()

class Workspace(BaseModel):

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    members = models.ManyToManyField(User, related_name='workspaces', blank=True)


    def __str__(self):
        return self.name
    



