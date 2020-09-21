from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from .serializer import YöneticiSerializer
from djangorest.permission import Issuperuser

# Create your views here.


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, Issuperuser])
def registerAdmin(request):
    data = request.data
    serializer = YöneticiSerializer(data=data)
    data["user"] = 1
    if serializer.is_valid():
        pass
    else:
        return Response(serializer.errors)

    u = User(username=data["username"],
             first_name=data["isim"],
             last_name=data["soyisim"],
             is_staff=True,
             is_superuser=True,
             email=request.user.email)

    u.set_password(data["password"])
    try:
        u.save()
        u.save(using=u.email)
    except BaseException as e:
        return Response({"success": "False",
                         "error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

    data["user"] = u.id
    serializer = YöneticiSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    token = Token.objects.create(user=u)
    return Response({"success": "true",
                     "username": u.username,
                     "user_id": u.id,
                     "token": token.key
                     }, status=status.HTTP_201_CREATED)
