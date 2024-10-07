from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    places_visited = models.IntegerField(default=0)
    looking_for = models.CharField(max_length=255, blank=True, null=True)
    diary_day_1 = models.TextField(blank=True, null=True)
    diary_day_2 = models.TextField(blank=True, null=True)
    diary_day_3 = models.TextField(blank=True, null=True)
    diary_day_4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'