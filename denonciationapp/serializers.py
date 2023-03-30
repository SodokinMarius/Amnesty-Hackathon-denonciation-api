from rest_framework import serializers

from .models import *
from authentication.models import User
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
from .models import Step, Publication, Petition

class CategorySerializer(serializers.ModelSerializer):
       class Meta:
            model = Category
            fields = ['id','name', 'description']
            read_only_fields = ['id']
            depth = 1

class ActorSerializer(serializers.ModelSerializer):
       class Meta:
            model = Category
            fields = ['id','type','name', 'category','address']
            read_only_fields = ['id']
            depth = 1


class TeamSerializer(serializers.ModelSerializer):
       class Meta:
            model = Category
            fields = ['id','name','contact', 'whatsapp','address','responsable']
            read_only_fields = ['id']
            depth = 1


class DenonciationSerializer(serializers.ModelSerializer):

    audio = serializers.ImageField(
    required=True,
    allow_empty_file=False,
    use_url=False,
    validators=[FileExtensionValidator(allowed_extensions=['mp3', 'aav'])]
        )
    
    file = serializers.ImageField(
    required=True,
    allow_empty_file=False,
    use_url=False,
    validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc','docx','txt'])]
)
    class Meta:
        model = Denonciation
        fields = '__all__'
        read_only_fields = ['id','team','category','created_at','updated_at']
        depth = 1
     
    def validate_pictures(self, value):
        """ Valide les images en vérifiant leur extension """
        valid_extensions = ['.jpg', '.jpeg', '.png']
        for img in value:
            ext = img.split('.')[-1]
            if not ext.lower() in valid_extensions:
                raise serializers.ValidationError(
                    "Seules les images de type JPG, JPEG ou PNG sont acceptées."
                )
        return value
    
    def validate_audio(self, value):
        """ Valide le fichier audio en vérifiant son extension """
        if value:
            ext = value.name.split('.')[-1]
            if not ext.lower() in ['mp3','aav']:
                raise serializers.ValidationError(
                    "Seuls les fichiers audio de type MP3  ou aav sont acceptés."
                )
        return value
    
    def validate_file(self, value):
        """ Valide le fichier en vérifiant son extension """
        if value:
            ext = value.name.split('.')[-1]
            if not ext.lower() in ['.pdf', '.doc', '.docx']:
                raise serializers.ValidationError(
                    "Seuls les fichiers de type PDF, DOC ou DOCX,TXT sont acceptés."
                )
        return value
    
    def create(self, validated_data):
        """ Traitement des fichiers avant la création de la denonciation """
        # Récupération des fichiers
        pictures = validated_data.pop('pictures', [])
        audio = validated_data.pop('audio', None)
        file = validated_data.pop('file', None)
        
        # Création de la denonciation
        denonciation = Denonciation.objects.create(**validated_data)
        
        # Traitement des images
        for img in pictures:
            # Traitement de chaque image, par exemple : 
            resized_img = resize_image(img) #resize the image
            save_to_disk(resized_img,'images/denonciation_pictures')#save image to disk
            denonciation.pictures.append(resized_img)
        
        # Traitement du fichier audio
        if audio:
            # Traitement du fichier audio, par exemple :
            trimmed_audio = trim_audio(audio)
            save_audio_to_disk(trimmed_audio)
            denonciation.audio = trimmed_audio
        
        # Traitement du fichier
        if file:
            # Traitement du fichier, par exemple :
            converted_file = convert_to_pdf(file)
            save_file_to_disk(converted_file)
            denonciation.file = converted_file
        
        # Sauvegarde de la denonciation
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
        fields = ['id', 'status', 'description', 'denonciation', 'actors', 'created_at', 'updated_at']
        read_only_fields = ['id','status','created_at','updated_at']
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






     