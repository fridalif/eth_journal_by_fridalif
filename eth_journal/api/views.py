from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpRequest, Http404
from .serializers import RegisterRequestsSerializer
import main.models as main_models

class RegisterRequestsAPIView(APIView):
    def get(self, request: HttpRequest):
        if request.user.is_superuser:
            raise Http404
        return Response(RegisterRequestsSerializer(main_models.RegisterRequests,many=True))