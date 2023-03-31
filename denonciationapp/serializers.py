from rest_framework import serializers

from .models import *
from authentication.models import Team
from django.core.validators import FileExtensionValidator

from utils.utils import (
resize_image, 
save_to_disk,
trim_audio,
save_audio_to_disk,
convert_to_pdf,
save_file_to_disk
)
from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
       class Meta:
            model = Category
            fields = ['id','name', 'description']
            read_only_fields = ['id']
            depth = 1

class ActorSerializer(serializers.ModelSerializer):
       class Meta:
            model = Actor
            fields = ['id','type','name', 'category','address']
            read_only_fields = ['id']
            depth = 1


class TeamSerializer(serializers.ModelSerializer):
       class Meta:
            model = Team
            fields = ['id','name','description','contact', 'whatsapp','address']
            read_only_fields = ['id']
            depth = 1


class DenonciationSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    denonciator_id = serializers.PrimaryKeyRelatedField(source='denonciator', queryset=Denonciator.objects.all(), required=True)
    actors = serializers.PrimaryKeyRelatedField(many=True, queryset=Actor.objects.all(), required=False)
    pictures = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png','jpeg'])]
    )
    audio = serializers.FileField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'aac','wav'])]
    )
    file = serializers.FileField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc','docx','txt'])]
    )
    status = serializers.SerializerMethodField()


    def get_status(self, obj):
        return str(obj.status)
    
    class Meta:
        model = Denonciation
        fields = '__all__'
        read_only_fields = ['id', 'category', 'team', 'status', 'updated_at']
        depth = 1

    def create(self, validated_data):
        pictures = validated_data.pop('pictures', [])
        audio = validated_data.pop('audio', None)
        file = validated_data.pop('file', None)
        actors = validated_data.pop('actors', [])

        denonciation = Denonciation.objects.create(**validated_data)

        denonciation.pictures = pictures
        denonciation.audio = audio
        denonciation.file = file

        if actors:
            denonciation.actors.set(actors)
        
        denonciation.save()
        return denonciation
    
    def update(self, instance, validated_data):
        """ Traitement des fichiers avant la mise à jour de la denonciation """
        # Récupération des fichiers
        pictures = validated_data.pop('pictures', None)
        audio = validated_data.pop('audio', None)
        file = validated_data.pop('file', None)
        
        # Mise à jour des données de la denonciation
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Traitement des images
        if pictures is not None:
            instance.pictures = []
            for img in pictures:
                resized_img = resize_image(img) #resize the image
                save_to_disk(resized_img,'images/denonciation_pictures')#save image to disk
                instance.pictures.append(resized_img)
        
        # Traitement du fichier audio
        if audio is not None:
            trimmed_audio = trim_audio(audio)
            save_audio_to_disk(trimmed_audio)
            instance.audio = trimmed_audio

        
class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'description', 'denonciation', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at','updated_at']
        depth = 1


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ['id', 'type', 'content', 'administrator', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at','updated_at']
        depth = 1

class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = ['id', 'content', 'publication', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at','updated_at','user']
        depth = 1
    

class DenonciatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denonciator
        fields = ['id', 'first_name', 'last_name', 'phone', 'address', 'created_at', 'follow_code','updated_at']
        read_only_fields = ['id','created_at','updated_at','user']
        depth = 1


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'content', 'team','created_at', 'updated_at']
        read_only_fields = ['id','created_at','updated_at','team']
        depth = 1

class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sms
        fields = ['id', 'content', 'denonciator','created_at', 'updated_at']
        read_only_fields = ['id','created_at','updated_at','denonciator']
        depth = 1






     