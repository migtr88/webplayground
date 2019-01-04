from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Función para eliminar la imagen antigua del avatar 
def custom_upload_to(instance, filename):
    # accedemos a la antigua instancia, al anterior perfil antes de cambiar la imagen
    old_instance = Profile.objects.get(pk=instance.pk)
    # borramos la imagen 
    old_instance.avatar.delete()
    # Indicamos que guarde el fichero dentro de profiles con su propio nombre
    return 'profiles/' + filename 

# Create your models here.
# Creamos un modelo profile de usuario 
class Profile(models.Model):
    # Relación oneToOne indica al modelo que solo puede haber un relacion de un solo perfil con un solo usuario
    # no 2 perfiles para un solo usuario , ni 2 usuarios para 1 perfil
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # Para ahorrar espacio de almacenamiento solo guardaremos la imagen de usuario más reciente, y borraremos las anteriores
    avatar = models.ImageField(upload_to = custom_upload_to, null = True, blank =True)
    bio = models.TextField(null = True, blank = True)
    link = models.URLField(max_length = 200, null = True, blank = True)

    class Meta: 
        ordering = ['user__username']
    
# Vamos a crear una señal para evitar el caso de que un usuario se registrará pero no accediera nunca, no llegando a crearse un perfil
# Para ello crearemos una signal para que se cree automaticamente un perfil al registrarse un usuario 
# Para llamarla necesitamos un decorador
@receiver(post_save, sender = User)
def ensure_profile_exists(sender, instance, **kwargs):
    # Como esta señal se va a ejecutar cada vez que se registre el usuario
    # nos aseguramos de entrar crear el perfil solo la 1º vez q se cree, en el caso de q se indique q la instancia se acaba de crear
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user = instance)
        print("Se acaba de crear un usuario y su perfil enlazado")