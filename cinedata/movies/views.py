from django.shortcuts import render

# Create your views here.



from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Movies

# Create your views here.
class MoviesListCreateView(APIView):


    def get(self,request,*args,**kwargs):

        movies =movies.objects.all()

        return Response(status=200)