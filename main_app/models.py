from django.db import models

# Create your models here.
        
class Variety(models.Model):
    name = models.CharField(max_length=140)
    latin = models.CharField(max_length=140, blank=True)
    edible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=140)
    city = models.CharField(max_length=140, blank=True)
    state = models.CharField(max_length=140, blank=True)
    country = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return self.name

class Share(models.Model):
    name = models.CharField(max_length=140)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Mushroom(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField(max_length=250, blank=True)
    shares = models.ManyToManyField(Share, blank=True)

    def __str__(self):
        return f'{self.variety.name} found in {self.place.name} on {self.date}'
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.URLField()
    mushroom = models.ForeignKey(Mushroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo of {self.mushroom}"

