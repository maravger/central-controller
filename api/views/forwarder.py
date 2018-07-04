from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes((AllowAny, ))
def post(request, slug=None):
    if slug == "app0":
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif slug == "app1":
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)