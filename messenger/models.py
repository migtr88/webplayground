from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta: 
        ordering = ['created']

class Thread(models.Model):
    users = models.ManyToManyField(User, related_name = 'threads')
    messages = models.ManyToManyField(Message)

    # Definimos la señal m2m_changed para que no se pueda añadir ningun mensaje al hilo si el usuario
    # no esta incluido en el hilo 
def messages_changed(sender, **kwargs):
    # Recuperamos la instancia(el thread), la acción, el conjunto q almacena los identificadores de los mensajes 
    instance = kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)
    print (instance, action, pk_set)
    # conjunto para almacenar los mensajes fraudulentos 
    false_pk_set = set()
    # En este bucle interceptamos el pk_set para buscar los mensajes q no añaden los usuarios del hilo y
    # los borramos 
    if action in "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print("Ups, ({}) no forma parte del hilo ".format(msg.user))
                false_pk_set.add(msg_pk)
    # buscar los mensajes de false_pk_set q no estan en el pk_set y los borra del pk_set
    pk_set.difference_update(false_pk_set)
m2m_changed.connect(messages_changed, sender = Thread.messages.through)