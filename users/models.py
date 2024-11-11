from django.contrib.auth.models import AbstractUser
from django.db import models

class Destinations(models.Model):
    destination = models.CharField(max_length=255)

class User(AbstractUser):
    visited_destinations = models.ManyToManyField(Destinations, through='Visit', related_name='visited_by')

    def __str__(self):
        return self.username
   
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    looking_for = models.CharField(max_length=255, blank=True, null=True)
    diary_day_1 = models.TextField(blank=True, null=True)
    diary_day_2 = models.TextField(blank=True, null=True)
    diary_day_3 = models.TextField(blank=True, null=True)
    diary_day_4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE, related_name='visits')
    visited_on = models.DateField(auto_now_add=True)
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('user', 'destination'),)
        verbose_name = "Visit"
        verbose_name_plural = "Visits"
    
class ProfilePhoto(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    profile_picture = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f'Photo for {self.user.username}'
