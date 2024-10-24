from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer,RegisterUserSerializer,UserProfileSerializer,UserProfile,VisitSerializer,Visit,DestinationsSerializer,Destinations
from django.shortcuts import render, redirect
from .forms import ProfilePhotoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfilePhotoForm  
from django.shortcuts import get_object_or_404
from barcelonaBE.settings import OPENWEATHERMAP_API_KEY
import requests


@api_view(['GET', 'POST'])
# @csrf_exempt
@permission_classes([permissions.IsAuthenticated])
def profile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)

    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user_profile = user_profile 
            photo.save() 
            return JsonResponse({'file_path': photo.profile_picture.url}, status=201)
        return JsonResponse({'errors': form.errors}, status=400) 

    
    photos = user_profile.photos.all() 
    photo_urls = [photo.profile_picture.url for photo in photos] 

    response_data = {
        'profile_pictures': photo_urls 
    }
    return JsonResponse(response_data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "detail": "Submit your credentials using a POST request to obtain a token."
        })
        
        
class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer()
        return Response(serializer.data)
    
    
class UserProfileView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        user_id = self.kwargs.get('id')
        return UserProfile.objects.get(user__id=user_id)

    def get(self, request, *args, **kwargs):
        # print(request.headers)
        try:
            profile = self.get_object()
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VisitView(generics.ListCreateAPIView):
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id'] 
        return Visit.objects.filter(user_profile__user__id=user_id) 

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        user_profile = UserProfile.objects.get(user__id=user_id)
        serializer.save(user_profile=user_profile)
        
        
class WeatherView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        api_key = OPENWEATHERMAP_API_KEY  
        city = 'Barcelona'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric' 

        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            return Response(weather_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Could not fetch weather data'}, status=status.HTTP_400_BAD_REQUEST)
        
class DestinationsList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        destinations=Destinations.objects.all()
        serializer = DestinationsSerializer(destinations,many=True)
        return Response(serializer.data)
        