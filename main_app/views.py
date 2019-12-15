from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def mushrooms_index(request):
    return render(request, 'mushrooms/index.html', {"mushrooms": mushrooms})

class Mushroom:  # Note that parens are optional if not inheriting from another class
  def __init__(self, variety, place, date, note, images):
    self.variety = variety
    self.place = place
    self.date = date
    self.note = note
    self.images = images

mushrooms = [
    Mushroom(variety="Shaggy Mane", place="My backyard", date="12/12/2019", note="Looks shaggy", images=[] )
]