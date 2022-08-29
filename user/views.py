import jwt

from django.shortcuts import render

from django.db.models import Q


from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from student.models import StudentDetail

from user.models import User
from user.serializers import ChangeUserPassword,  CurrentUserSerializer, LogoutSerializer, StudentLoginSerializer, UserSerializer, MyTokenObtainPairSerializer

from student.paginations import StudentPaginaition

# Create your views here.
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserCreateApi(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted = False)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(id = pk)
        user.is_deleted = True
        user.is_active = False
        user.save()
        return Response({"detail":"User is deleted"},status=status.HTTP_200_OK)

class ObtainTokenPairWithUsernameView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer    


class UserDetails(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        user = request.user
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)        

class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangeUserPassword
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, query=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class StudentLoginCreateAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentLoginSerializer

    def perform_create(self, serializer):
        instance=serializer.save()
        id = self.request.POST['student_id']
        if id:
            student=StudentDetail.objects.get(id=id)
            student.student_user=instance
            student.save()

class StudentListApi(generics.ListAPIView):
    model = User
    queryset = User.objects.filter(role="Student")      
    permission_classes = (IsAuthenticated,)
    pagination_class = StudentPaginaition
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name','last_name']



class StaffListApi(generics.ListAPIView):
    model = User
    queryset = User.objects.filter(Q(role="Admin") | Q(role = "User"))      
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StudentPaginaition
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name','last_name','username']

