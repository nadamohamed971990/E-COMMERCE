# Django Import
from base64 import urlsafe_b64encode
from collections import UserString
from django.template.loader import render_to_string
import queue
from rest_framework import generics
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

# Rest Framework JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Local Import
from base.models import *
from base.serializers import UserSerializer, UserSerializerWithToken, AddImgSerializer



# Create a new Image
# @api_view(['POST'])
# def createImg(request):
#     user = request.user
#     Img = AddImg.objects.create(
#         user=user,
#         image="Image ",
#     )

#     serializer = AddImgSerializer(Img, many=False)
#     return Response(serializer.data)

# JWT Views
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['message'] = "Hello Proshop"
        # ...
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# SHOP API
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/<id>',
        '/api/users',
        '/api/users/register',
        '/api/users/login',
        '/api/users/profile',
        "/api/users/password_reset/",
    ]
    return Response(routes)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    mail = "Thanks for register"
    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            password = make_password(data['password']),
        )
        send_mail(
            mail,
            "Thanks for register",
            settings.EMAIL_HOST_USER,
            [data['email']],
            fail_silently=False,
        )
        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)

    except:
        message = {"detail": "User with this email is already registered"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != "":
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response("User was deleted")

# class PasswordResetView(GenericAPIView):
#         """
#         Calls Django Auth PasswordResetForm save method.

#         Accepts the following POST parameters: email
#         Returns the success/fail message.
#         """
#         serializer_class = PasswordResetSerializer
#         permission_classes = (AllowAny,)

#         def post(self, request, *args, **kwargs):
#                 # Create a serializer with request.data
#                 serializer = self.get_serializer(data=request.data)
#                 serializer.is_valid(raise_exception=True)

#                 serializer.save() # <----- Code from above (TokenGenerator) will be called inside this .save() method
#                 # Return the success message with OK HTTP status
#                 return Response(
#                         {"detail": _("Password reset e-mail has been sent.")},
#                         status=status.HTTP_200_OK
#                 )



# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def passwordResetRequest(request,pk):
#     userForReset = User.objects.get(id=pk)
#     user.email = data['email']
#     if userForReset in user.email :
#         data = password_reset_form.cleaned_data['email']
#         associated_users = User.objects.filter(Q(email=data))
#             # You can use more than one way like this for resetting the password.
#             # ...filter(Q(email=data) | Q(username=data))
#             # but with this you may need to change the password_reset form as well.
#         if associated_users.exists():
#             for user in associated_users:
#                 subject = "Password Reset Requested"
#                 email_template_name = "admin/accounts/password/password_reset_email.txt"
#                 c = {
#                     "email": user.email,
#                     'domain': domain,
#                     'site_name': 'Interface',
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "user": user,
#                     'token': default_token_generator.make_token(user),
#                     'protocol': 'http',
#                 }
#                 email = render_to_string(email_template_name, c)
#                 try:
#                     send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
#                 except BadHeaderError:
#                     return HttpResponse('Invalid header found.')
#                 return redirect("/core/password_reset/done/")
#     password_reset_form = PasswordResetForm()
#     return render(context={"password_reset_form": password_reset_form})

# @api_view(['POST'])
# def passwordResetConfirm(request):

