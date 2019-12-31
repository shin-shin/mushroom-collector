from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
        
class Variety(models.Model):
    variety_name = models.CharField(max_length=140)
    latin = models.CharField(max_length=140, blank=True)
    edible = models.BooleanField(default=False)

    def __str__(self):
        return self.variety_name

class Place(models.Model):
    place_name = models.CharField(max_length=140)
    city = models.CharField(max_length=140, blank=True)
    state = models.CharField(max_length=140, blank=True)
    country = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return self.place_name

class Share(models.Model):
    share_name = models.CharField(max_length=140)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.share_name


class Mushroom(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField(max_length=250, blank=True)
    shares = models.ManyToManyField(Share, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.variety} found in {self.place} on {self.date}'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'mushroom_id': self.id})
    
    def get_note(self):
        if len(self.note) == 0:
            return
        return self.note

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    mushroom = models.ForeignKey(Mushroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo of {self.mushroom} @{self.url}"

