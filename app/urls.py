from django.urls import path
from app.views import  ArtistList, ClientRegistration,WorkList

urlpatterns = [
    path('api/works/', WorkList.as_view(), name='work-list'),
    path('api/artists/', ArtistList.as_view(), name='artist-list'),
    path('api/register/', ClientRegistration.as_view(), name='ClientRegistration'),
]