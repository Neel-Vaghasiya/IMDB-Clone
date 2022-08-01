from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User

from .serializers import RegistrationSerializer

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data)

@api_view(['POST',])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def login_view(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                email = user.email
                id = user.id
                # if not Token.objects.filter(user=user).exists():
                #     Token.objects.create(user=user)
                token, created = Token.objects.get_or_create(user=user)
                
                contextdata = {"token":token.key, "username": username, "email": email, "id": id}
                return Response(contextdata)
            else:
                return Response({"error": "Password is incorrect"})
        except:
            return Response({"error": "User not found"})

