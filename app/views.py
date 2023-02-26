from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Client, Artist, Work
from api.serializers import ClientSerializer, ArtistSerializer, WorkSerializer

class WorkList(generics.ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated,]

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics, permissions, serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Artist, Work

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

class WorkList(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

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

@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)

class ArtistList(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Work.objects.all()
        work_type = self.request.query_params.get('work_type')
        artist_name = self.request.query_params.get('artist_name')
        if work_type:
            queryset = queryset.filter(work_type=work_type)
        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)
        return queryset

class ArtistList(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

class ClientRegistration(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
