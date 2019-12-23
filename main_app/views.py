from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Mushroom
import os

# Create your views here.

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def mushrooms_index(request):
    mushrooms = Mushroom.objects.all()
    return render(request, 'mushrooms/index.html', {"mushrooms": mushrooms})
def mushrooms_details(request, mushroom_id):
    print("mushroom_id", mushroom_id)
    mushroom = Mushroom.objects.get(id=mushroom_id)
    return render(request, 'mushrooms/details.html', {"mushroom": mushroom})

class Test(ListView):
    model = Mushroom

