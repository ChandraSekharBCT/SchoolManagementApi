from django.http.response import Http404
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import ProfileSerializer, RegisterSerializer,LoginSerializer
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "data":serializer.data,
            "status":status.HTTP_200_OK,
            "msg":"Account created successfully,please contact admin"
            })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data
        profile = Profile(user=request.user,first_name=data.get('first_name'),last_name=data.get('last_name'),DOB=data.get('DOB'),image=data.get('image'))
        profile.save()
        return Response("Account Created successfully")
        
    def put(self,request):
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            raise Http404
        serializer = ProfileSerializer(profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
