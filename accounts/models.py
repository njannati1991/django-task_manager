from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    national_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11, unique=True)
    birthday = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.username
    

class UserAvatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avatars')
    avatar = models.ImageField(upload_to='avatars/')
    
    is_active = True
    is_prime = False

    def __str__(self):
        return self.user.username
