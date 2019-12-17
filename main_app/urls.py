from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('mushrooms/<int:mushroom_id>/', views.mushrooms_details, name='details'),
    path('mushrooms/', views.mushrooms_index, name='mushrooms'),
]