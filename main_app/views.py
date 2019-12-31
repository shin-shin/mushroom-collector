from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Mushroom, Variety, Place, Photo, Share
from .forms import MushroomForm, VarietyForm, PlaceForm, PhotoForm, ShareForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import os
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'mycoco'

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')

@login_required    
def mushrooms_index(request):
    print("mushrooms_index starts!")
    mushrooms = Mushroom.objects.filter(user=request.user)
    print("first mushroom photos: ", mushrooms[0].photo_set)
    return render(request, 'mushrooms/index.html', {"mushrooms": mushrooms})

from django.forms.models import inlineformset_factory

@login_required 
def mushroom_update(request, pk):
    print('mushroom_update called, pk=', pk)
    mushroom = Mushroom.objects.get(id=pk)
    variety = Variety.objects.get(id=mushroom.variety.id)
    place = Place.objects.get(id=mushroom.place.id)
    
    if request.method == "POST":
        variety.edible = False
        if 'edible' in request.POST:
            variety.edible = True


        variety.variety_name = request.POST.get("variety_name")
        variety.latin = request.POST.get("latin")
        variety.save()
        
        place.place_name = request.POST.get("place_name")
        place.city = request.POST.get("city")
        place.state = request.POST.get("state")
        place.country = request.POST.get("country")
        place.save()
        
        mushroom.date = request.POST.get("date")
        mushroom.note = request.POST.get("note")
        mushroom.save()
        return redirect('mushrooms') 
    else:

        mush = {
            "variety_name": variety.variety_name,
            "latin": variety.latin,
            "edible": variety.edible,
            "place_name": place.place_name,
            "city": place.city,
            "state": place.state,
            "country": place.country,
            "date": mushroom.date.strftime("%Y-%m-%d"),
            "nice_date": mushroom.date,
            "note": mushroom.note,
        }
        context = {
            "object": mush,
        }
        return render(request, "mushrooms/mushroom_update.html", context)

@login_required 
def mushroom_form(request, *pk):
    print('multiple forms: starts! request.variety_name=', request.POST.get('variety_name'))
    print('request.user ', request.user)
    if request.method == "POST":
        # add user field too
        edible = False
        if 'edible' in request.POST:
            edible = True

        variety = Variety(variety_name=request.POST.get('variety_name'), latin=request.POST.get('latin'), edible=edible)
        variety.save()
        place = Place(place_name=request.POST.get('place_name'), city=request.POST.get('city'), state=request.POST.get('state'), country=request.POST.get('country'))
        place.save()
        mushroom = Mushroom(variety=variety, place=place, date=request.POST.get('date'), note=request.POST.get('note'), user=request.user)
        mushroom.save()
        return redirect('mushrooms')


            # model_instance = form.save(commit=False)
            # model_instance.save()
        

    else:
        context = {
            "test": 42
        }
    return render(request, "mushrooms/mushroom_new.html")

class MushroomDelete(LoginRequiredMixin, DeleteView):
    model = Mushroom
    success_url = '/mushrooms/'


@login_required
def mushrooms_details(request, mushroom_id):
    print("mushroom_id", mushroom_id)
    mushroom = Mushroom.objects.get(id=mushroom_id)
    not_shared_on = Share.objects.exclude(id__in = mushroom.shares.all().values_list('id'))
    return render(request, 'mushrooms/details.html', {
        "mushroom": mushroom, 
        "variety": mushroom.variety,
        "shares": not_shared_on
        })

@login_required 
def add_photo(request, mushroom_id):
    print("mushroom_id", mushroom_id)
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to mushroom_id or mushroom (if you have a mushroom object)
            photo = Photo(url=url, mushroom_id=mushroom_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('details', mushroom_id=mushroom_id)

class ShareCreate(LoginRequiredMixin, CreateView):
    model = Mushroom
    success_url = '/mushrooms/'
class ShareUpdate(LoginRequiredMixin, UpdateView):
    model = Mushroom
    success_url = '/mushrooms/'
class ShareList(LoginRequiredMixin, ListView):
    model = Mushroom
    success_url = '/mushrooms/'
class ShareDelete(LoginRequiredMixin, DeleteView):
    model = Mushroom
    success_url = '/mushrooms/'

@login_required
def add_share(request, mushroom_id, share_id):
    print("add_share: ", mushroom_id, share_id)
    # mushroom = Mushroom.objects.get(id=pk)
    # share = Share.objects.get(id=share_id)
    #mushroom.share
    Mushroom.objects.get(id=mushroom_id).shares.add(share_id)

    return redirect('details', mushroom_id=mushroom_id)