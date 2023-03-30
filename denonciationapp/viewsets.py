from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import DenonciationSerializer
from .models import Denonciation

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

class DenonciationViewSet(viewsets.ModelViewSet):
    queryset = Denonciation.objects.all()
    serializer_class = DenonciationSerializer
    parser_classes = [MultiPartParser,FormParser,FileUploadParser]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        denonciation = self.get_object()
        serializer = self.get_serializer(denonciation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        denonciation = self.get_object()
        denonciation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
