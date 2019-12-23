from django.contrib import admin
from .models import Mushroom, Variety, Photo, Place, Share
# Register your models here.
admin.site.register(Mushroom)
admin.site.register(Variety)
admin.site.register(Photo)
admin.site.register(Place)
admin.site.register(Share)