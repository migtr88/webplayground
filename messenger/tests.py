from django.test import TestCase
from django.contrib.auth.models import User 
from .models import Message,Thread

# Create your tests here.

class ThreadTestCase(TestCase):
    def setUp(self):
        # Creamos usuarios de prueba
        self.user1 = User.objects.create_user('user1',None, 'test1234')
        self.user2 = User.objects.create_user('user2',None, 'test1234')
        self.user3 = User.objects.create_user('user3',None, 'test1234')
        # Creamos una instancia de thread 
        self.thread = Thread.objects.create()

    # Añadimos usuarios a la instancia thread
    def test_add_users_to_thread(self):
        self.thread.users.add(self.user1,self.user2)
        # Comprobamso que la longitud del campo usuarios es 2 
        self.assertEqual(len(self.thread.users.all()),2)
    # test que recupera un hilo ya existente a partir de sus usuarios 
    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1,self.user2)
        threads = Thread.objects.filter(users = self.user1).filter(users = self.user2)
        #Comprobamos si el hilo es el q hemos recuperado
        self.assertEqual(self.thread, threads[0]) 
    
    # Test q comprueba que no existe un hilo cuando los usuarios no forman parte de el
    # debe devolver un query set vacíon 
    def test_filter_non_existed_thread(self):
        threads = Thread.objects.filter(users = self.user1).filter(users = self.user2)
        #Comprobamos si el hilo es el q hemos recuperado, debe tener 0 usuarios
        self.assertEqual(len(threads), 0) 

    # Test que comprueba la existencia de un mensaje
    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1,self.user2)
        message1 = Message.objects.create(user=self.user1, content = "Hola")
        message2 = Message.objects.create(user=self.user2, content = "Muy bien")
        # añadimos mensajes a la hebra
        self.thread.messages.add(message1,message2) 
        # Comprobamos q haya 2 mensajes 
        self.assertEqual(len(self.thread.messages.all()),2)
        # Mostramos los mensajes en un bucle 
        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))


    #Test para demostrar q un usuario q no esta en el hilo puede añadir un mensaje al hilo
    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content = "Hola")
        message2 = Message.objects.create(user=self.user2, content = "Muy bien")
        message3 = Message.objects.create(user=self.user3, content = "I'am a spy")
        self.thread.messages.add(message1,message2,message3)
        self.assertEqual(len(self.thread.messages.all()),2)