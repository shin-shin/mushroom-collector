from django.forms import ModelForm
from django.forms import modelform_factory
from .models import Mushroom, Variety, Place, Photo, Share

MushroomForm = modelform_factory(Mushroom, fields=('date', 'note'))

VarietyForm = modelform_factory(Variety, fields=('variety_name', 'latin', 'edible'))

PlaceForm = modelform_factory(Place, fields=('place_name', 'city', 'state', 'country'))

PhotoForm = modelform_factory(Photo, fields=('url',))

ShareForm = modelform_factory(Share, fields=('share_name', 'url'))