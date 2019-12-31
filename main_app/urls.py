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
    
    path('shares/', views.ShareList.as_view(), name='shares_index'),
    path('shares/create/', views.ShareCreate.as_view(), name='shares_create'),
    path('shares/<int:pk>/update/', views.ShareUpdate.as_view(), name='shares_update'),
    path('shares/<int:pk>/delete/', views.delete_share, name='shares_delete'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
]