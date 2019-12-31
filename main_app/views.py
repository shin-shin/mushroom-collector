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
    mushrooms = Mushroom.objects.filter(user=request.user)
    return render(request, 'mushrooms/index.html', {"mushrooms": mushrooms})

from django.forms.models import inlineformset_factory

# a way to have form with many models
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





# class VarietyCreate(LoginRequiredMixin, CreateView):
#     model = Variety
#     fields = ['name', 'latin', 'edible']
#     def form_valid(self, form):
#         # Assign the logged in user
#         form.instance.user = self.request.user
#         # Let the CreateView do its job as usual
#         return super().form_valid(form)

# class MushroomCreate(LoginRequiredMixin, CreateView):
#     model = Mushroom
#     fields = ['date', 'note']
#     def form_valid(self, form):
#         # Assign the logged in user
#         form.instance.user = self.request.user
#         # Let the CreateView do its job as usual
#         return super().form_valid(form)

# class MushroomUpdate(LoginRequiredMixin, UpdateView):
#     model = Mushroom
#     fields = ['variety', 'place', 'note', 'shares']

class MushroomDelete(LoginRequiredMixin, DeleteView):
    model = Mushroom
    success_url = '/mushrooms/'




@login_required
def mushrooms_details(request, mushroom_id):
    print("mushroom_id", mushroom_id)
    mushroom = Mushroom.objects.get(id=mushroom_id)
    return render(request, 'mushrooms/details.html', {"mushroom": mushroom, "variety": mushroom.variety})


