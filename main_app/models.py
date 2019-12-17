from django.db import models

# Create your models here.
class Mushroom(models.Model):
    variety = models.CharField(max_length=140)
    place = models.CharField(max_length=140)
    date = models.DateField()
    note = models.TextField(max_length=250)
    images = models.URLField()

    def __str__(self):
        return self.variety
