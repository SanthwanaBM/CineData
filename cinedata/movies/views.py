from django.shortcuts import render

# Create your views here.



from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Movies
from .serializer import MoviesListRetrieveSerializer, MoviesCreateUpdateSerializer

import json

from django.shortcuts import get_object_or_404

from rest_framework import authentication

from rest_framework.permissions import AllowAny

from authentication.permissions import IsAdmin,IsUser

from rest_framework_simplejwt import authentication


# Create your views here.
class MoviesListCreateView(APIView):

    http_method_names=['get','post']

    # ths is the serializer for create and update view

    authentication_classes = [authentication.JWTAuthentication]
    
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

     # ths is the serializer for create and update view


    get_serializer_class = MoviesListRetrieveSerializer

     # ths is the serializer for reterive and list view

    post_serializer_class =  MoviesCreateUpdateSerializer

    def get_permissions(self):

        if self.request.method =='GET':

            return [AllowAny()]
        
        elif self.request.method == 'POST':

            return [IsAdmin()]

        return super().get_permissions()
    
    def get(self,request,*args,**kwargs):

        movies =Movies.objects.filter(active_status=True)

        serializer =self.get_serializer_class(movies,many=True)

        return Response(data=serializer.data,status=200)
    
    def post(self,request,*args,**kwargs):

        print(request.data.get('cast'))

        print(request.data)

        serializer = self.post_serializer_class(data=request.data)

        if serializer.is_valid():

            movie = serializer.save()

            # loads function for 

            cast_ids = json.loads(request.data.get('cast',[])) 

            movie.cast.set(cast_ids)



            return Response(data={'msg':'movie crated successfully'},status=200)
        
        return Response(data=serializer.errors,status=400)
    

class MoviesRetrieveUpdateDestroyView(APIView):

    get_serializer_class = MoviesListRetrieveSerializer

    put_serializer_class = MoviesCreateUpdateSerializer

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        serializer = self.get_serializer_class(movie)

        return Response(data=serializer.data,status=200)  

    def put(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid) 

        serializer = self.put_serializer_class(instance=movie,data=request.data,partial=True)

        if serializer.is_valid():

            movie_obj= serializer.save()

            cast = request.data.get('cast')

            if cast :

                cast_ids = json.loads(cast,[])


# data = json.loads(request.body.decode('utf-8'))

                movie_obj.cast.set(cast_ids)

            return Response(data={'msg': 'course updated successfully'},status=200)

        return Response(data=serializer.errors,status=400)   


    def delete(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid) 

        Movies.active_status=False

        movie.save()

        return Response(data={'msg':'deleted successfully'},status=200)