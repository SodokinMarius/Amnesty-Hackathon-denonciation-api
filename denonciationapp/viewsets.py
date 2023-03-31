from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from .models import *
from datetime import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import permissions, status, viewsets
from utils.enums import *
class DenonciationViewSet(viewsets.ModelViewSet):
    queryset = Denonciation.objects.all()
    serializer_class = DenonciationSerializer
    parser_classes = [MultiPartParser,FormParser,FileUploadParser]
    permission_classes = [permissions.AllowAny]
    

    def perform_create(self, serializer):
        denounced = serializer.save()
        # Ajouter les acteurs à la relation many-to-many
        actors = self.request.data.get('actors', [])
        denounced.actors.set(actors)


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
    
    """_summary_
    THis function take a denonciation status as parameter and returns 
    all Denonciations whatever the type after treating
    """
    
    def getAllDenonciationCategorizedByStatus(self,retrieved_status):
        
        denonciations = self.queryset.filter(status=retrieved_status).order_by('-created_at')
       
       # Add public election and their options to a dict
       
        denonciations = [
                {
                    'denonciation': DenonciationSerializer(denonciation).data,
                    'actors': ActorSerializer(denonciation.actors.all(),many=True).data,
                    'steps' :  StepSerializer (Step.objects.filter(denonciation=denonciation),many=True).data
                }
                for denonciation in denonciations
            ]

        print("Denonciation ==============+++++>",denonciations)
        return denonciations
    

    def changeDenonciationStatus(self, change_to:str):
        denonciation = self.get_object()
        current_date = timezone.now()
        response ={}
        if(
            denonciation.status == change_to 
            or 
         denonciation.status == StatutDenoEnum.COMPLETED.value
        ):
            response = {"message" : "This denonciation can not be set to this status"}
            print("la denonciation cliqué :{} et ses etapes : {}".format(denonciation,Step.objects.filter(denonciation=denonciation).count()))
       
        else:
            denonciation.status = change_to
           
            denonciation.save()
            serializer = DenonciationSerializer(denonciation)
            response = {
                'data' : serializer.data,
                'message' : "Denonciation has been changed successfully  to {}!".format(change_to)
            }

            # Envoie ici de notification dans l'APP et par SMS au denonciator
        return response

    """_summary_
    THis function take a denonciation status as parameter and returns 
    all Denonciations whatever the type after treating
    """
    
    def getAllDenonciationCategorizedByPriority(self,priority):
        
        denonciations = self.queryset.filter(priority=priority).order_by('-created_at')
       
       # Add public election and their options to a dict
       
        denonciations = [
                {
                    'denonciation': DenonciationSerializer(denonciation).data,
                    'actors': ActorSerializer(denonciation.actors.all(),many=True).data,
                    'steps' :  StepSerializer (Step.objects.filter(denonciation=denonciation),many=True).data
                }
                for denonciation in denonciations
            ]

        print("Denonciation ==============+++++>",denonciations)
        return denonciations

    
    @action(methods=['get'], detail=False, url_path="completed", url_name="completed")
    def completed(self, request):
        
        response_data = self.getAllDenonciationCategorizedByStatus(StatutDenoEnum.COMPLETED.value)
        
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    
    @action(methods=['get'], detail=False, url_path="", url_name="pending")
    def pending(self, request):
        
        response_data = self.getAllDenonciationCategorizedByStatus(StatutDenoEnum.PENDING.value)
        
        return Response(data=response_data, status=status.HTTP_200_OK)
        
    @action(methods=['get'], detail=False, url_path="", url_name="in_progress")
    def in_progress(self, request):
        
        response_data = self.getAllDenonciationCategorizedByStatus(StatutDenoEnum.IN_PROGESS.value)
        
        return Response(data=response_data, status=status.HTTP_200_OK)
    
        
    @action(methods=['get'], detail=False, url_path="", url_name="rejected")
    def rejected(self, request):
        
        response_data = self.getAllDenonciationCategorizedByStatus(StatutDenoEnum.REJECTED.value)
        
        return Response(data=response_data, status=status.HTTP_200_OK)
 
 
    @action(methods=['get'], detail=False, url_path="", url_name="urgent")
    def urgent(self, request):
        
        response_data = self.getAllDenonciationCategorizedByPriority(PriorityDenoEnum.IN_PROGESS.value)
        
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="", url_name="passed")
    def passed(self, request):
        
        response_data = self.getAllDenonciationCategorizedByPriority(PriorityDenoEnum.PASSED.value)
        
        return Response(data=response_data, status=status.HTTP_200_OK)
        
             
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


    def list(self, request, *args, **kwargs):
        user = request.user
        categories = self.queryset

        categories = [
                {
                    'category': CategorySerializer(category).data,
                    'denonciations': DenonciationSerializer(DenonciationSerializer.objects.filter(category=category.id),many=True).data
                }
                for category in categories
            ]
        
        
        return Response(data=categories, status=status.HTTP_200_OK)

    
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]



class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAuthenticated]


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]
     
    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['administrator'] = user
    
        serializer.save()

class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer


class DenonciatorViewSet(viewsets.ModelViewSet):
    queryset = Denonciator.objects.all()
    serializer_class = DenonciatorSerializer
    permission_classes = [permissions.AllowAny]


