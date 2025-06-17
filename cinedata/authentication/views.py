from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework.response import Response

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import AllowAny

class LoginView(APIView):

     http_method_names = ['post']

     def post(self,request,*args,**kwargs):
          
          username = request.data.get('username')

          password = request.data.get('password')

          user = authenticate(username=username,password=password)

          if user:
               
               access_token = RefreshToken.for_user(user).access_token

               return Response(data={'access_token':str(access_token)})
          
          return Response(data={'msg':'invalid credential'},status=401)


class UserRegistration(APIView):

     http_method_names = ['post']

     authentication_classes = [JWTAuthentication]

     permission_classes = [AllowAny]