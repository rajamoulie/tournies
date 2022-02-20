from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sport(models.Model) :
    sport = models.CharField(max_length=50)

    def __str__(self) :
        return self.sport

class Tourney(models.Model) :
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=50)
    location = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ['-updated', '-created']
    
    def __str__(self) :
        return self.name

class Message(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tourney = models.ForeignKey(Tourney, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ['-updated', '-created']

    def __str__(self) :
        return self.body