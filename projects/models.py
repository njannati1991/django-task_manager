from django.db import models

from django.utils.text import slugify
from core.models import BaseModel
from workspaces.models import Workspace


class Project(BaseModel):

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    descriptions = models.TextField(null=True, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    @classmethod
    def user_total_projects(cls, user):
        return Project.objects.filter(workspace__memberships__members = user).count()
    


