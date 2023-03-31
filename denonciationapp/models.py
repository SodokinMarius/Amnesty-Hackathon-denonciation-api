from django.db import models
from utils.enums import *

from django.contrib.postgres.fields import ArrayField
from authentication.models import Administrator


class Denonciator(models.Model):
    phone = models.CharField(max_length=15,unique=True,null=False)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    address =  models.JSONField(verbose_name="Localisation")   
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now_add=True) 

    REQUIRED_FIELDS=['address','phone']
 
    def __str__(self):
        return '{self.phone} {self.first_name} {self.last_name}'
   
    def get_user_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    def get_address(self):
        return f'{self.address}'
    
    def has_module_perms(self, app_label) :
        return True
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Catégorie de la denonciation")

    def __str__(self) -> str:
        return  self.name


class Actor(models.Model):
    type = models.CharField(max_length=200,choices=VictimTypeEnum.items(),default=VictimTypeEnum.INDIVIDU.value) 
    name = models.TextField(verbose_name="Description de l'acteur")
    category = models.CharField(max_length=200,choices=ActorCategoryEnum.items(),default=ActorCategoryEnum.WITNESS.value) 
    address =  models.JSONField(verbose_name="Localisation")

    def __str__(self) -> str:
            return  self.name
    

class Team(models.Model):
    name = models.TextField(verbose_name="Description de l'Equipe")
    contact = models.TextField(verbose_name="contact de l'Equipe")
    whatsapp = models.TextField(verbose_name="Numéro whatsapp de l'Equipe")
    address =  models.JSONField(verbose_name="Localisation")
    responsable = models.OneToOneField(to=Administrator,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return  self.name 


class Denonciation(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(verbose_name="Description de la denonciation",null=True,blank=True)
    #pictures = ArrayField(models.ImageField(upload_to='images/denonciations_images'))
    pictures = models.ImageField(upload_to='denonciations_images',null=True,blank=True)
    audio =  models.FileField(upload_to='denonciation_audios',blank=True,null=True)
    file =  models.FileField(upload_to='denonciation_files',blank=True,null=True)
    status = models.CharField(max_length=200,choices=StatutDenoEnum.items(),default=StatutDenoEnum.PENDING.value)
    address =  models.JSONField(verbose_name="Localisation") 
    priority = models.CharField(max_length=200,choices=PriorityDenoEnum.items(),default=PriorityDenoEnum.PASSED.value) 
    denonciator = models.ForeignKey(to=Denonciator,on_delete=models.SET_NULL,null=True) 
    category = models.ForeignKey(to=Category,on_delete=models.SET_NULL,null=True) 
    team = models.ForeignKey(to=Team,on_delete=models.SET_NULL,null=True) 
    actors = models.ManyToManyField(to=Actor,related_name="actors")
    created_at=models.DateTimeField(auto_now_add=True)  
    updated_at=models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return  self.title
    
class Step(models.Model):
    description = models.CharField(max_length=200)
    denonciation = models.ForeignKey(to=Denonciation,on_delete=models.SET_NULL,null=True) 
    created_at=models.DateTimeField(auto_now_add=True)  
    updated_at=models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return  f'{self.status} {self.denonciation}'

class Publication(models.Model):  
    type = models.CharField(max_length=200,choices=TypePublishEnumEnum.items(),default=TypePublishEnumEnum.ACTUALITE.value) 
    content = models.TextField(verbose_name="Description de la publication")
    administrator = models.ForeignKey(to=Administrator,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)  
    updated_at=models.DateTimeField(auto_now_add=True) 
     
    def __str__(self) -> str:
            return  f'{self.type} {self.content}'


class Petition(models.Model):
    content = models.TextField(verbose_name="Contenu de la publication")
    publication = models.ForeignKey(to=Publication,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(to=Denonciator,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)  
    updated_at=models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
            return  f'{self.content} {self.publication} {self.user}'




