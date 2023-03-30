from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .serializers import LogoutSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .serializers import (
    AdminCreateSerializer as  UserCreateSerializer,
    
)
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from authentication.models import Administrator, UserActivationCode

from rest_framework.views import APIView
from djoser.views import UserViewSet

from utils.send_email import send_email_to
from utils.random_password_generate import random_pass_generator


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = request.data
        user = request.user
        setattr(user,'actual_connected_espace',None)
        user.save()

        return Response(data=data,status=status.HTTP_204_NO_CONTENT)

from django.contrib.sites.shortcuts import get_current_site


class AccountUserViewset(UserViewSet):
    queryset = Administrator.objects.all()
    serializer_class = UserCreateSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def perform_create(self, serializer):
        current_site = get_current_site(self.request)
        user = serializer.save()
        activation_code = random_pass_generator()

        user_activation_code = UserActivationCode.objects.create(user=user, activation_code=activation_code)
        user_activation_code.save()
        activation_message = f"Salut  {user.first_name} {user.last_name}.\n\nVous recevez cet message car vous venez de vous inscrire sur l'application DenonceApp, veuillez activer votre comptre en utilisant le code suivant :\n\n{activation_code}"

        send_email_to("Account activation ", activation_message, [user.email])


class CustomAdministratorViewset(generics.UpdateAPIView):
    queryset = Administrator.objects.all()
    serializer_class = UserCreateSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super(CustomAdministratorViewset, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def patch(self, request):
        data = request.data
        user = request.user
        print(user)
        print(data)
        for key, value in data.items():
            if key!='password':
                setattr(user,key,value)

        print(request)
        user.save()

        data =  UserCreateSerializer(user, context=self.get_serializer_context()).data

        return Response(data, status=status.HTTP_200_OK)



class UserActivationView(APIView):

    def get_permissions(self):
        method = self.request.method
        if method in ('POST', 'PUT', 'PATCH'):
           return [permissions.IsAdminUser()]
        else:

            return []

    def get (self, request, email, code):

        user = Administrator.objects.filter(email=email).first()
        if not user:
            return Response({'message': "User not found"})

        user_activation = UserActivationCode.objects.filter(user=user, usable=True).first()
        if not user_activation:
            return Response({'message': "User activation code not found"})

        if user_activation.activation_code == code:
            user.is_active = True
            user.save()
            user_activation.usable=False
            user_activation.save()

            activation_message = f"Salut {user.first_name} {user.last_name}\n\nVotre compte a été crée et activé avec succès sur DenonceApp !"
            send_email_to("Account Activated", activation_message, [user.email])
            return Response({'message': 'Account activted successfully'})
        else:
            return Response({'message':'Invalid activation code'})
        

"""
class DenunciatorUserViewset(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = DenunciatorCreateSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super(CustomAdministratorViewset, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def patch(self, request):
        data = request.data
        user = request.user
        print(user)
        print(data)
        for key, value in data.items():
            if key!='password':
                setattr(user,key,value)

        print(request)
        user.save()

        data =  UserCreateSerializer(user, context=self.get_serializer_context()).data

        return Response(data, status=status.HTTP_200_OK)"""
