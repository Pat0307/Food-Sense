from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('create/', views.createProfile, name="createProfile"),
    path('profile/', views.profile, name="profile"),
    path('favorites_list/', views.favorites_list, name="favorites_list"),
    path('favorite/<int:id>', views.favorite, name="favorite"),
    path('delete_favorite/', views.delete_favorite, name='delete_favorite'),
]
