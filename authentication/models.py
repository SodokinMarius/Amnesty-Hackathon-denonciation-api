from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager,PermissionsMixin)


class Team(models.Model):
    name = models.CharField(max_length=225,unique=True, default="PINCIPAL")
    description = models.TextField(verbose_name="Description de l'Equipe",null=True)
    contact = models.TextField(verbose_name="contact de l'Equipe")
    whatsapp = models.TextField(verbose_name="Numéro whatsapp de l'Equipe")
    address =  models.JSONField(verbose_name="Localisation")

    def __str__(self) -> str:
        return  self.name
    

class UserManager(BaseUserManager):
    def create_user(self, email="admin@gmail.com", password=None,**kwargs):
        if not email:
            raise ValueError("Users must have an email address")
    
        
        user = self.model(
            email=self.normalize_email(email),
         
           **kwargs
        )        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,password,**kwargs):
        if not email:
            raise ValueError("Users must have an email address")
       
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            **kwargs
        
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Administrator(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="Adresse mail de l'Administrateur",unique=True)
    profil = models.ImageField(upload_to="admin_images",default="static/images/default_user.png")
    type_admin = models.CharField(default="AdminType",max_length=225)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address =  models.JSONField(verbose_name="Localisation")
    team = models.ForeignKey(to=Team,on_delete=models.SET_NULL,null=True)
    is_team_responsable = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)   
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['password','address','profil','first_name','last_name']
    
    objects = UserManager() 


    def __str__(self) -> str:
        return self.email + " : " + self.activation_code

    def has_perm(self, perm, obj=None):
            return self.is_admin
    
    def get_user_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    def get_address(self):
        return f'{self.address}'
    
    def has_module_perms(self, app_label) :
        return True

class UserActivationCode(models.Model):
    user = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True)
    activation_code = models.CharField(max_length=20, null=True)
    usable = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.user.email + " : " + self.activation_code

