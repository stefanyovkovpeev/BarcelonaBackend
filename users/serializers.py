from rest_framework import serializers
from .models import User,UserProfile,Visit,Destinations
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class DestinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinations
        fields = ['destination','id']
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name']
    

class VisitSerializer(serializers.ModelSerializer):
    destination_name = serializers.ReadOnlyField(source='destination.destination')

    class Meta:
        model = Visit
        fields = ['destination', 'destination_name', 'visited_on', 'review']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'country', 'bio',
            'looking_for', 'diary_day_1', 'diary_day_2', 'diary_day_3', 'diary_day_4'
        ]
        read_only_fields = ['user']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        data.update({
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        })

        return data
    
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user    
