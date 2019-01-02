from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Creamos un modelo profile de usuario 
class Profile(models.Model):
    # Relación oneToOne indica al modelo que solo puede haber un relacion de un solo perfil con un solo usuario
    # no 2 perfiles para un solo usuario , ni 2 usuarios para 1 perfil
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to = 'profiles', null = True, blank =True)
    bio = models.TextField(null = True, blank = True)
    link = models.URLField(max_length = 200, null = True, blank = True)
    