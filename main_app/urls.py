from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('mushrooms/<int:mushroom_id>/add_share/<int:share_id>', views.add_share, name='add_share'),
    path('mushrooms/<int:mushroom_id>/', views.mushrooms_details, name='details'),
    path('mushrooms/<int:pk>/update', views.mushroom_update, name='mushroom_update'),
    path('mushrooms/<int:pk>/delete', views.MushroomDelete.as_view(), name='mushroom_delete'),
    path('mushrooms/<int:mushroom_id>/add-photo', views.add_photo, name='add_photo'),
    path('mushrooms/new-mushroom', views.mushroom_form, name='new_mushroom'),
    path('mushrooms/', views.mushrooms_index, name='mushrooms'),
    
    # path('mushrooms/new-mushroom', views.mushroom_new, name='new_mushroom'),
    # path('mushrooms/new-mushroom', views.MushroomCreate.as_view(), name='new_mushroom'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
]