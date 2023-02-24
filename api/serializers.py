from app.models import Client,Work,Artist
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics, permissions, serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Client, Artist, Work

# Serializer classes for the models
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    works = WorkSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

# API endpoint for showing works with filtering and search options
class WorkList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Work.objects.all()
        work_type = request.GET.get('work_type')
        artist_name = request.GET.get('artist_name')
        if work_type:
            queryset = queryset.filter(work_type=work_type)
        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)
        serializer = WorkSerializer(queryset, many=True)
        return Response(serializer.data)

# API endpoint for user registration
@api_view(['POST'])
def registration(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'username and password are required'})
    user = User.objects.create_user(username, password=password)
    client = Client.objects.create(name=username, user=user)
    serializer = ClientSerializer(client)
    return Response(serializer.data)

# Signal to create a Client object after a new user registration
@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)

# API endpoint for showing all artists
class ArtistList(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
