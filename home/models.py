from pyexpat import model
from django.db import models
from django.db.models import Q

# Create your models here.

class imdb(models.Model):
    movie_name = models.CharField(unique= True, max_length=256, null = True, blank= True)

    class Meta:
        indexes = [
            models.Index(fields=['movie_name'], condition=Q(movie_name__isnull=False), name='movie_title_index'),
        ]
